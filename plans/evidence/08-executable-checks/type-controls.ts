export function length(value: string | string[]): number {
  return value.length;
}
export function first(values: number[]): number | undefined {
  return values[0];
}
export function guarded(values: number[]): string | undefined {
  const value = values[0];
  return value === undefined ? undefined : value.toFixed(2);
}
export function unsafe(values: number[]): string {
  // @ts-expect-error Unchecked array access can produce undefined.
  return values[0].toFixed(2);
}
export function assertOnly(input: unknown): { value: string } {
  return input as { value: string };
}
