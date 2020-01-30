==================
Perfect Forwarding
==================

Perfect forwarding is a way for a programmer to design a generic wrapper
function in their C++ programs. However, few examples show how to use it in a
real scenario. Instead of explaining what a C++ `perfect forwarding` is, this
article tries to collect use cases about using it.

Factory Pattern
---------------

.. code-block:: cpp

    #include <iostream>
    #include <utility>
    #include <string>
    #include <memory>

    struct PostgresqlConfig { /* implementation */ };
    struct MysqlConfig { /* implementation */ };

    template <typename DB>
    class Session {
    public:
        void connect(const std::string url) {
            static_cast<DB*>(this)->connect(url);
        }
    };

    class Postgresql : public Session<Postgresql> {
    private:
        PostgresqlConfig config_;
    public:
        Postgresql(PostgresqlConfig c) : config_(c) {}

        void connect(const std::string url) {
            std::cout << "Connecting to Postgresql..." << std::endl;
            // connecting
        }
    };

    class Mysql : public Session<Mysql> {
    private:
        MysqlConfig config_;
    public:
        Mysql(MysqlConfig c) : config_(c) {}

        void connect(const std::string url) {
            std::cout << "Connecting to Mysql..." << std::endl;
            // connecting
        }
    };

    /**
     * An example of Perfect Forwarding
     */
    template <typename S, typename C>
    std::shared_ptr<S> SessionFactory(C&& c) {
        return std::make_shared<S>(std::forward<C>(c));
    }

    using PostgresSession = Session<Postgresql>;
    using MysqlSession = Session<Mysql>;
    using PostgresPtr = std::shared_ptr<PostgresSession>;
    using MysqlPtr = std::shared_ptr<MysqlSession>;

    int main(int argc, char *argv[]) {

        PostgresqlConfig pc;
        MysqlConfig mc;

        PostgresPtr ps = SessionFactory<Postgresql>(pc);
        MysqlPtr ms = SessionFactory<Mysql>(mc);

        ps->connect("postgresql://...");
        ms->connect("mysql://...");
        return 0;
    }
