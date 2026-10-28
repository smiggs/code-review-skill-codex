package invalid.example.package10.fixturesupport;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.util.List;

import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;

/**
 * Contract test for the jpa-membership fixture. The harness copies either the
 * clean base or the defective head into invalid.example.package10.fixture
 * before running; the fixture supplies its own entities and service class. These tests are enabled only when the harness passes -Dpackage10fixture=true.
 */
class ParentReaderContractTest {

    private static EntityManagerFactory factory() throws Exception {
        String database = "fixture_" + System.nanoTime();
        StandardServiceRegistryBuilder registry = new StandardServiceRegistryBuilder()
            .applySetting("hibernate.connection.url", "jdbc:h2:mem:" + database + ";DB_CLOSE_DELAY=-1")
            .applySetting("hibernate.connection.driver_class", "org.h2.Driver")
            .applySetting("hibernate.connection.username", "sa")
            .applySetting("hibernate.connection.password", "")
            .applySetting("hibernate.dialect", "org.hibernate.dialect.H2Dialect")
            .applySetting("hibernate.hbm2ddl.auto", "create-drop");
        MetadataSources sources = new MetadataSources(registry.build())
            .addAnnotatedClass(Class.forName("invalid.example.package10.fixture.ParentReader$FixtureUser"))
            .addAnnotatedClass(Class.forName("invalid.example.package10.fixture.ParentReader$FixtureOrder"));
        return sources.buildMetadata().getSessionFactoryBuilder().build();
    }

    private static void seed(EntityManagerFactory factory) throws Exception {
        Class<?> userType = Class.forName("invalid.example.package10.fixture.ParentReader$FixtureUser");
        Class<?> orderType = Class.forName("invalid.example.package10.fixture.ParentReader$FixtureOrder");
        Constructor<?> userCtor = userType.getDeclaredConstructor(String.class);
        userCtor.setAccessible(true);
        Constructor<?> orderCtor = orderType.getDeclaredConstructor(userType, int.class);
        orderCtor.setAccessible(true);
        try (EntityManager manager = factory.createEntityManager()) {
            manager.getTransaction().begin();
            Object ada = userCtor.newInstance("Ada");
            Object ben = userCtor.newInstance("Ben");
            Object cyd = userCtor.newInstance("Cyd");
            manager.persist(ada);
            manager.persist(ben);
            manager.persist(cyd);
            manager.persist(orderCtor.newInstance(ada, 10));
            manager.persist(orderCtor.newInstance(ada, 11));
            manager.persist(orderCtor.newInstance(ben, 20));
            manager.getTransaction().commit();
        }
    }

    @Test
    @Timeout(180)
    @EnabledIfSystemProperty(named = "package10fixture", matches = "true")
    void staleParentsKeepTheirRequestedMembership() throws Exception {
        EntityManagerFactory factory = factory();
        try {
            seed(factory);
            List<?> parents = (List<?>) Class.forName("invalid.example.package10.fixture.ParentReader")
                .getMethod("readStaleParents", EntityManagerFactory.class)
                .invoke(null, factory);
            StringBuilder joined = new StringBuilder();
            for (Object parent : parents) {
                joined.append(parent).append(' ');
            }
            String names = joined.toString();
            assertTrue(names.contains("Cyd"),
                "every requested parent must be preserved, including parents with no related records");
            assertTrue(names.contains("Ada") && names.contains("Ben"),
                "the parents with related records remain in the page");
        } finally {
            factory.close();
        }
    }
}
