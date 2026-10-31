/*
 * Invented compiler-family fixture for static C++ object machinery.
 * A global derived object records construction and cleanup through an opaque
 * hook. Virtual methods expose each compiler's ordinary table and symbol
 * conventions. This is diagnostic code, not a game reconstruction or a match.
 */

typedef unsigned int u32;

/* The implementation is deliberately outside this translation unit. */
extern "C" void producer_event(u32 event);

class ProducerBase {
public:
    ProducerBase();
    virtual ~ProducerBase();
    virtual u32 value() const;
};

class ProducerDerived : public ProducerBase {
public:
    ProducerDerived();
    virtual ~ProducerDerived();
    virtual u32 value() const;
};

/* Record the base portion's construction. */
ProducerBase::ProducerBase()
{
    producer_event(1);
}

/* Record the base portion's cleanup. */
ProducerBase::~ProducerBase()
{
    producer_event(2);
}

/* Return an easily distinguished base implementation value. */
u32 ProducerBase::value() const
{
    return 11;
}

/* Record the derived portion after the base has been constructed. */
ProducerDerived::ProducerDerived()
{
    producer_event(3);
}

/* Record the derived portion before automatic base cleanup. */
ProducerDerived::~ProducerDerived()
{
    producer_event(4);
}

/* Return an easily distinguished derived implementation value. */
u32 ProducerDerived::value() const
{
    return 22;
}

/* Exercise ordinary virtual dispatch through a caller-supplied base object. */
extern "C" u32 producer_read_value(const ProducerBase* object)
{
    return object->value();
}

/* Its lifetime requests the compiler's normal static initialization support. */
ProducerDerived producer_global;
