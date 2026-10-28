package invalid.example.package10;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

import javax.sql.DataSource;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.interceptor.TransactionAspectSupport;
import org.springframework.transaction.support.TransactionSynchronizationManager;

/**
 * Spring Framework 6.1.14 checks for the proxy-mode, invocation-path,
 * visibility, and readOnly contracts quoted in reference/java.md. H2 backs the
 * transaction manager; these are synthetic checks of the audited version, not
 * claims about other versions or configurations.
 */
class SpringProxyTransactionTest {

    static final List<String> OBSERVATIONS = new CopyOnWriteArrayList<>();

    static boolean insideTransaction() {
        return TransactionSynchronizationManager.isActualTransactionActive();
    }

    public interface Inspectable {
        String tx();

        String viaSelf();
    }

    public static class InterfaceService implements Inspectable {
        @Transactional
        public String tx() {
            OBSERVATIONS.add("annotatedPublic:" + insideTransaction());
            return "tx";
        }

        @Override
        public String viaSelf() {
            OBSERVATIONS.add("plainPublic:" + insideTransaction());
            this.tx();
            return "self";
        }
    }

    public static class ConcreteService {
        @Transactional
        public String publicTx() {
            OBSERVATIONS.add("concretePublic:" + insideTransaction());
            return "public";
        }

        @Transactional
        String packageTx() {
            OBSERVATIONS.add("packageVisible:" + insideTransaction());
            return "package";
        }
    }

    public static class PrivateService {
        @Transactional
        private void hidden() {
            OBSERVATIONS.add("privateMethod:" + insideTransaction());
        }

        public void caller() {
            OBSERVATIONS.add("beforePrivate:" + insideTransaction());
            this.hidden();
        }
    }

    public static class ReaderService {
        @Transactional(readOnly = true)
        public String reading() {
            boolean hint = TransactionAspectSupport.currentTransactionStatus().isReadOnly();
            OBSERVATIONS.add("readOnlyHint:" + hint);
            return String.valueOf(hint);
        }
    }

    public static class PlainService {
        public String write() {
            OBSERVATIONS.add("plainBean:" + insideTransaction());
            return "plain";
        }
    }

    @Configuration
    @EnableTransactionManagement
    static class TxConfig {
        @Bean
        DataSource dataSource() {
            String url = "jdbc:h2:mem:tx_" + System.nanoTime() + ";DB_CLOSE_DELAY=-1";
            return new SimpleDriverDataSource(new org.h2.Driver(), url, "sa", "");
        }

        @Bean
        PlatformTransactionManager transactionManager(DataSource dataSource) {
            return new DataSourceTransactionManager(dataSource);
        }

        @Bean
        InterfaceService interfaceService() {
            return new InterfaceService();
        }

        @Bean
        ConcreteService concreteService() {
            return new ConcreteService();
        }

        @Bean
        PrivateService privateService() {
            return new PrivateService();
        }

        @Bean
        ReaderService readerService() {
            return new ReaderService();
        }

        @Bean
        PlainService plainService() {
            return new PlainService();
        }
    }

    @Test
    @Timeout(60)
    void publicInterfaceMethodIsAdvisedThroughAJdkProxy() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            Inspectable proxy = context.getBean(Inspectable.class);
            assertTrue(AopUtils.isJdkDynamicProxy(proxy), "interface bean runs a JDK dynamic proxy");
            assertEquals("tx", proxy.tx());
            assertEquals(List.of("annotatedPublic:true"), OBSERVATIONS,
                "the annotated public method ran inside an active transaction");
        }
    }

    @Test
    @Timeout(60)
    void selfInvocationBypassesTheProxyAndStartsNoTransaction() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            Inspectable proxy = context.getBean(Inspectable.class);
            assertEquals("self", proxy.viaSelf());
            assertEquals(List.of("plainPublic:false", "annotatedPublic:false"), OBSERVATIONS,
                "this.tx() ran the annotated body outside any transaction");
        }
    }

    @Test
    @Timeout(60)
    void classProxyAdvisesPackageVisibleMethodsUnderSpring6Defaults() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            ConcreteService proxy = context.getBean(ConcreteService.class);
            assertTrue(AopUtils.isCglibProxy(proxy), "interface-less bean runs a CGLIB proxy");
            assertEquals("package", proxy.packageTx());
            assertEquals(List.of("packageVisible:true"), OBSERVATIONS,
                "since 6.0 package-visible methods are transactional for class-based proxies");
        }
    }

    @Test
    @Timeout(60)
    void privateTransactionalMethodRunsOutsideAnyTransaction() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            PrivateService proxy = context.getBean(PrivateService.class);
            proxy.caller();
            assertEquals(List.of("beforePrivate:false", "privateMethod:false"), OBSERVATIONS,
                "the private annotated method ran with no transaction on the call path");
            NoSuchMethodException notRoutable = assertThrows(NoSuchMethodException.class, () ->
                proxy.getClass().getDeclaredMethod("hidden"));
            System.out.println("OBSERVED private-method routing evidence: " + notRoutable.getMessage());
        }
    }

    @Test
    @Timeout(60)
    void readOnlyIsVisibleAsAHintOnTheTransactionStatus() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            ReaderService proxy = context.getBean(ReaderService.class);
            assertEquals("true", proxy.reading());
            assertEquals(List.of("readOnlyHint:true"), OBSERVATIONS,
                "the readOnly hint is recorded on the transaction status");
        }
    }

    @Test
    @Timeout(60)
    void unannotatedBeanWorksWithoutTransactionSupport() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            PlainService bean = context.getBean(PlainService.class);
            assertEquals("plain", bean.write());
            assertEquals(List.of("plainBean:false"), OBSERVATIONS,
                "clean control: an unannotated bean runs without container transaction machinery");
        }
    }

    @Test
    @Timeout(60)
    void annotatedConcretePublicMethodIsAdvisedThroughTheClassProxy() {
        OBSERVATIONS.clear();
        try (AnnotationConfigApplicationContext context =
            new AnnotationConfigApplicationContext(TxConfig.class)) {
            ConcreteService proxy = context.getBean(ConcreteService.class);
            assertEquals("public", proxy.publicTx());
            assertEquals(List.of("concretePublic:true"), OBSERVATIONS,
                "clean control: concrete public method advised normally");
        }
    }
}
