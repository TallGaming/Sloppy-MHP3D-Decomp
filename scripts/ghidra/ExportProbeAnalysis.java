// Export bounded analysis for Bucket 3B. Pseudocode and automatic types are hypotheses.
// @category MHP3Research

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import com.google.gson.GsonBuilder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

public class ExportProbeAnalysis extends GhidraScript {
    private String digest(byte[] data) throws Exception {
        StringBuilder result = new StringBuilder();
        for (byte value : MessageDigest.getInstance("SHA-256").digest(data)) {
            result.append(String.format("%02x", value & 255));
        }
        return result.toString();
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 1) throw new IllegalArgumentException("Expected one export path");
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("scope", "static analysis hypotheses; no source match or runtime proof");
        report.put("language_id", currentProgram.getLanguageID().toString());
        report.put("compiler_spec_id", currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        report.put("image_base", currentProgram.getImageBase().toString());
        report.put("executable_sha256", currentProgram.getExecutableSHA256());
        List<Object> blocks = new ArrayList<>();
        for (MemoryBlock block : currentProgram.getMemory().getBlocks()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("name", block.getName()); row.put("start", block.getStart().toString());
            row.put("end", block.getEnd().toString()); row.put("size", block.getSize());
            row.put("initialized", block.isInitialized()); row.put("execute", block.isExecute());
            blocks.add(row);
        }
        report.put("memory_blocks", blocks);
        TreeMap<String, Function> selected = new TreeMap<>();
        List<Object> targets = new ArrayList<>();
        for (long value : new long[]{0x08830550L, 0x08830654L}) {
            Address address = toAddr(value);
            int size = value == 0x08830550L ? 52 : 36;
            byte[] bytes = new byte[size]; currentProgram.getMemory().getBytes(address, bytes);
            Map<String, Object> target = new LinkedHashMap<>();
            target.put("address", address.toString()); target.put("size", size);
            target.put("memory_sha256", digest(bytes));
            Function function = getFunctionAt(address);
            target.put("function_at_start", function == null ? null : function.getEntryPoint().toString());
            if (function != null) selected.put(function.getEntryPoint().toString(), function);
            List<Map<String, Object>> calls = new ArrayList<>();
            ReferenceIterator references = currentProgram.getReferenceManager().getReferencesTo(address);
            while (references.hasNext()) {
                Reference reference = references.next();
                if (!reference.getReferenceType().isCall()) continue;
                Function caller = getFunctionContaining(reference.getFromAddress());
                Map<String, Object> call = new LinkedHashMap<>();
                call.put("site", reference.getFromAddress().toString());
                call.put("caller", caller == null ? null : caller.getEntryPoint().toString());
                calls.add(call);
                if (caller != null) selected.put(caller.getEntryPoint().toString(), caller);
            }
            calls.sort(Comparator.comparing(row -> (String)row.get("site")));
            target.put("call_references", calls); targets.add(target);
        }
        report.put("targets", targets);
        for (long value : new long[]{0x08830584L, 0x088305B4L, 0x088305DCL, 0x08830604L, 0x08830678L, 0x088306D4L}) {
            Function function = getFunctionAt(toAddr(value));
            if (function != null) selected.put(function.getEntryPoint().toString(), function);
        }
        DecompInterface decompiler = new DecompInterface();
        if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException("Cannot open decompiler");
        List<Object> functions = new ArrayList<>();
        try {
            for (Function function : selected.values()) {
                monitor.checkCancelled();
                Map<String, Object> row = new LinkedHashMap<>();
                row.put("entry", function.getEntryPoint().toString()); row.put("name", function.getName());
                row.put("signature_hypothesis", function.getPrototypeString(false, false));
                row.put("body_min", function.getBody().getMinAddress().toString());
                row.put("body_max", function.getBody().getMaxAddress().toString());
                row.put("body_address_count", function.getBody().getNumAddresses());
                DecompileResults result = decompiler.decompileFunction(function, 30, monitor);
                row.put("decompile_completed", result.decompileCompleted());
                row.put("error", result.getErrorMessage());
                row.put("pseudocode_hypothesis", result.decompileCompleted()
                        ? result.getDecompiledFunction().getC() : null);
                functions.add(row);
            }
        } finally { decompiler.dispose(); }
        report.put("functions", functions);
        Path path = Path.of(args[0]);
        Files.writeString(path, new GsonBuilder().setPrettyPrinting().disableHtmlEscaping().create().toJson(report)
                          + "\n", StandardCharsets.UTF_8, java.nio.file.StandardOpenOption.CREATE_NEW);
        println("BUCKET_03B_EXPORT_COMPLETE " + functions.size() + " bounded functions/callers");
    }
}
