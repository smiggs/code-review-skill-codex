package invalid.example.package10;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicLong;

import org.hibernate.Hibernate;
import org.hibernate.LazyInitializationException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.proxy.HibernateProxy;
import org.hibernate.resource.jdbc.spi.StatementInspector;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

/**
 * Hibernate ORM 6.4.10.Final with H2 2.2.224 checks for the persistence
 * contracts quoted in reference/java.md. This is synthetic evidence about the
 * audited versions, not a claim about other providers or releases.
 */
class JpaFetchTest {

    /** Counts executed statements; registered by class name in the service registry. */
    public static final class SqlStatements implements StatementInspector {
        static final AtomicLong COUNT = new AtomicLong();
        static final List<String> SQL = Collections.synchronizedList(new ArrayList<>());

        static void reset() {
            COUNT.set(0);
            SQL.clear();
        }

        @Override
        public String inspect(String sql) {
            COUNT.incrementAndGet();
            SQL.add(sql);
            return sql;
        }
    }

    @Entity(name = "TestUser")
    public static class TestUser {
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        Long id;

        String name;

        @OneToMany(mappedBy = "owner", fetch = FetchType.EAGER)
        List<TestOrder> orders = new ArrayList<>();

        public TestUser() {
        }

        public TestUser(String name) {
            this.name = name;
        }

        public Long getId() {
            return id;
        }

        public String name() {
            return name;
        }

        @Override
        public boolean equals(Object other) {
            if (this == other) {
                return true;
            }
            // The conventional identifier getter must be used, not the field: a
            // proxy's interceptor serves the identifier without initialising,
            // while the field is null and other accessors may initialise.
            return other instanceof TestUser user && id != null && id.equals(user.getId());
        }

        @Override
        public int hashCode() {
            return Objects.hash(id);
        }
    }

    @Entity(name = "TestOrder")
    public static class TestOrder {
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        Long id;

        int total;

        @ManyToOne(fetch = jakarta.persistence.FetchType.LAZY)
        TestUser owner;

        public TestOrder() {
        }

        public TestOrder(TestUser owner, int total) {
            this.owner = owner;
            this.total = total;
        }
    }

    private SessionFactory factory() {
        String database = "pkg10_" + System.nanoTime();
        StandardServiceRegistryBuilder registry = new StandardServiceRegistryBuilder()
            .applySetting("hibernate.connection.url", "jdbc:h2:mem:" + database + ";DB_CLOSE_DELAY=-1")
            .applySetting("hibernate.connection.driver_class", "org.h2.Driver")
            .applySetting("hibernate.connection.username", "sa")
            .applySetting("hibernate.connection.password", "")
            .applySetting("hibernate.dialect", "org.hibernate.dialect.H2Dialect")
            .applySetting("hibernate.hbm2ddl.auto", "create-drop")
            .applySetting("hibernate.session_factory.statement_inspector",
                SqlStatements.class.getName());
        return new MetadataSources(registry.build())
            .addAnnotatedClass(TestUser.class)
            .addAnnotatedClass(TestOrder.class)
            .buildMetadata()
            .getSessionFactoryBuilder()
            .build();
    }

    private void seed(SessionFactory factory) {
        try (Session session = factory.openSession()) {
            session.beginTransaction();
            TestUser ada = new TestUser("Ada");
            TestUser ben = new TestUser("Ben");
            TestUser cyd = new TestUser("Cyd");
            session.persist(ada);
            session.persist(ben);
            session.persist(cyd);
            session.persist(new TestOrder(ada, 10));
            session.persist(new TestOrder(ada, 11));
            session.persist(new TestOrder(ben, 20));
            session.getTransaction().commit();
        }
    }

    @Test
    @Timeout(60)
    void eagerCollectionLoadsEveryParentThroughSeparateSelects() {
        SessionFactory factory = factory();
        seed(factory);
        try (Session session = factory.openSession()) {
            SqlStatements.reset();
            List<TestUser> users = session.createQuery("select u from TestUser u order by u.id",
                TestUser.class)
                .list();
            assertEquals(3, users.size());
            users.forEach(user -> user.orders.size());
            assertEquals(4, SqlStatements.COUNT.get(),
                "fixture evidence: 1 query for the list plus one eager select per parent (N+1)");
        } finally {
            factory.close();
        }
    }

    @Test
    @Timeout(60)
    void joinFetchIssuesOneQueryButDropsChildlessParents() {
        SessionFactory factory = factory();
        seed(factory);
        try (Session session = factory.openSession()) {
            SqlStatements.reset();
            List<TestUser> users = session.createQuery(
                "select u from TestUser u join fetch u.orders order by u.id", TestUser.class)
                .list();
            users.forEach(user -> user.orders.size());
            assertEquals(1, SqlStatements.COUNT.get(), "join fetch is a single query");
            assertEquals(List.of("Ada", "Ben"), users.stream().map(TestUser::name).toList(),
                "inner fetch join drops Cyd, who has no orders");
        } finally {
            factory.close();
        }
    }

    @Test
    @Timeout(60)
    void leftJoinFetchIssuesOneQueryAndPreservesChildlessParents() {
        SessionFactory factory = factory();
        seed(factory);
        try (Session session = factory.openSession()) {
            SqlStatements.reset();
            List<TestUser> users = session.createQuery(
                "select u from TestUser u left join fetch u.orders order by u.id", TestUser.class)
                .list();
            users.forEach(user -> user.orders.size());
            assertEquals(1, SqlStatements.COUNT.get(), "left join fetch is a single query");
            List<String> names = users.stream().map(TestUser::name).toList();
            assertTrue(names.containsAll(List.of("Ada", "Ben", "Cyd")),
                "every parent is preserved, including childless Cyd");
            TestUser cyd = users.stream().filter(u -> u.name.equals("Cyd")).findFirst().orElseThrow();
            assertEquals(0, cyd.orders.size(), "Cyd has an empty collection, not null");
            System.out.println("OBSERVED left-join-fetch list size for 3 users holding 3 orders: "
                + users.size());
        } finally {
            factory.close();
        }
    }

    @Test
    @Timeout(60)
    void paginationWithCollectionFetchIsAppliedInMemoryNotInSql() {
        SessionFactory factory = factory();
        seed(factory);
        try (Session session = factory.openSession()) {
            SqlStatements.reset();
            List<TestUser> users = session.createQuery(
                "select u from TestUser u left join fetch u.orders order by u.id", TestUser.class)
                .setMaxResults(2)
                .list();
            users.forEach(user -> user.orders.size());
            List<String> statements = List.copyOf(SqlStatements.SQL);
            assertEquals(1, statements.size(), "one query handled the page");
            assertFalse(statements.get(0).toLowerCase().contains("limit"),
                "setMaxResults was applied in memory (no LIMIT was pushed to H2)");
            assertEquals(2, users.size(), "two parent entities returned for the request");
            System.out.println("OBSERVED paged left-join-fetch composition: "
                + users.stream().map(TestUser::name).toList()
                + " with orders " + users.stream().map(u -> u.orders.size()).toList());
        } finally {
            factory.close();
        }
    }

    @Test
    @Timeout(60)
    void identifierEqualityWorksAcrossTheProxyWithoutInitialisingIt() {
        SessionFactory factory = factory();
        seed(factory);
        Long adaId;
        try (Session session = factory.openSession()) {
            adaId = session.createQuery("select u.id from TestUser u where u.name = 'Ada'", Long.class)
                .uniqueResult();
        }
        TestUser found;
        try (Session session = factory.openSession()) {
            found = session.get(TestUser.class, adaId);
        }
        try (Session session = factory.openSession()) {
            TestUser proxied = session.getReference(TestUser.class, adaId);
            assertInstanceOf(HibernateProxy.class, proxied, "getReference returns a proxy");
            assertFalse(Hibernate.isInitialized(proxied), "proxy starts uninitialised");
            proxied.getId();
            assertFalse(Hibernate.isInitialized(proxied),
                "reading the identifier does not initialise the proxy");
            assertTrue(found.equals(proxied),
                "identifier-based equality matches the detached and proxied instance");
            assertFalse(Hibernate.isInitialized(proxied),
                "identifier equality left the proxy uninitialised");
            boolean wasInitial = !Hibernate.isInitialized(proxied);
            assertTrue(proxied.equals(found),
                "identifier equality holds with the proxy as receiver (observed direction)");
            System.out.println("OBSERVED proxied.equals(found) initialised the proxy: "
                + Hibernate.isInitialized(proxied));
            boolean stillInitial = Hibernate.isInitialized(proxied);
            String constant = found.getClass().getName() + "@" + found.hashCode();
            int proxyHash = proxied.hashCode();
            assertEquals(found.hashCode(), proxyHash,
                "constant identifier hashCode stays consistent across instances");
            System.out.println("OBSERVED proxy hashCode initialised the proxy: "
                + (Hibernate.isInitialized(proxied) && wasInitial)
                + " (constant recorded as " + constant + ")");
        } finally {
            factory.close();
        }
    }

    @Test
    @Timeout(60)
    void lazyCollectionReadsOutsideSessionFail() {
        SessionFactory factory = factory();
        seed(factory);
        TestOrder recent;
        Session openBriefly = factory.openSession();
        try {
            openBriefly.beginTransaction();
            recent = openBriefly.createQuery(
                "select o from TestOrder o where o.owner.name = 'Ben' order by o.id",
                TestOrder.class)
                .setMaxResults(1)
                .uniqueResult();
            openBriefly.getTransaction().commit();
        } finally {
            openBriefly.close();
        }
        LazyInitializationException failure = assertThrows(LazyInitializationException.class,
            () -> recent.owner.name());
        assertTrue(failure.getMessage() != null);
        factory.close();
    }
}
