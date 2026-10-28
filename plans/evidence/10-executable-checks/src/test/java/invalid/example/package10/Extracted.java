package invalid.example.package10;

import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Path;

/** Loads the extracted, unmodified guide example classes for behaviour checks. */
public final class Extracted {
    private static volatile URLClassLoader loader;

    private Extracted() {
    }

    private static URL urlOf(Path classes) {
        try {
            return classes.toUri().toURL();
        } catch (java.net.MalformedURLException unreachable) {
            throw new IllegalStateException("extracted class directory URL", unreachable);
        }
    }

    /** Loader over .generated/guide-classes/release-21 relative to the module directory. */
    public static ClassLoader loader() {
        URLClassLoader current = loader;
        if (current == null) {
            synchronized (Extracted.class) {
                current = loader;
                if (current == null) {
                    Path classes = Path.of(".generated", "guide-classes", "release-21")
                        .toAbsolutePath()
                        .normalize();
                    if (!classes.resolve("UserDto.class").toFile().exists()) {
                        throw new IllegalStateException(
                            "Run plans/evidence/10-executable-checks/extract.py first; missing " + classes);
                    }
                    loader = current = new URLClassLoader(new URL[]{urlOf(classes)},
                        Extracted.class.getClassLoader());
                }
            }
        }
        return current;
    }

    public static Class<?> type(String name) throws ClassNotFoundException {
        return loader().loadClass(name);
    }

    public static Object invokeStatic(Class<?> type, String method, Class<?>[] parameterTypes,
                                      Object... arguments) throws ReflectiveOperationException {
        Method methodHandle = type.getDeclaredMethod(method, parameterTypes);
        methodHandle.setAccessible(true);
        try {
            return methodHandle.invoke(null, arguments);
        } catch (java.lang.reflect.InvocationTargetException failure) {
            throw failure;
        }
    }

    public static Object construct(Class<?> type, Class<?>[] parameterTypes, Object... arguments)
        throws ReflectiveOperationException {
        return type.getDeclaredConstructor(parameterTypes).newInstance(arguments);
    }
}
