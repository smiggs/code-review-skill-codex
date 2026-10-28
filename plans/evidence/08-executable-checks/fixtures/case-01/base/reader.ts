function readValue(data: unknown): string {
  if (typeof data !== 'object' || data === null ||
      !('value' in data) || typeof data.value !== 'string') {
    throw new Error('Expected a string value');
  }
  return data.value;
}

export { readValue };
