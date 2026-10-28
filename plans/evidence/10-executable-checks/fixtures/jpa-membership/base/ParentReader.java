package invalid.example.package10.fixture;

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

/** Supplies the stale parents for the housekeeping page. */
public class ParentReader {

    @Entity(name = "FixtureUser")
    public static class FixtureUser {
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        Long id;

        String name;

        @OneToMany(mappedBy = "holder", fetch = FetchType.EAGER)
        List<FixtureOrder> orders = new ArrayList<>();

        protected FixtureUser() {
        }

        public FixtureUser(String name) {
            this.name = name;
        }

        @Override
        public String toString() {
            return name;
        }
    }

    @Entity(name = "FixtureOrder")
    public static class FixtureOrder {
        @Id
        @GeneratedValue(strategy = GenerationType.AUTO)
        Long id;

        int total;

        @ManyToOne
        FixtureUser holder;

        protected FixtureOrder() {
        }

        public FixtureOrder(FixtureUser holder, int total) {
            this.holder = holder;
            this.total = total;
        }
    }

    public static List<FixtureUser> readStaleParents(EntityManagerFactory factory) {
        try (EntityManager manager = factory.createEntityManager()) {
            return manager.createQuery(
                "select u from FixtureUser u left join fetch u.orders order by u.id",
                FixtureUser.class)
                .getResultList();
        }
    }
}
