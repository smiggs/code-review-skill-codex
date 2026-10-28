function readValue(data: unknown): string {
  if (typeof data !== 'object' || data === null ||
      !('value' in data)) {
    throw new Error('Expected a string value');
  }
  return (data as { value: string }).value;
}

export { readValue };
