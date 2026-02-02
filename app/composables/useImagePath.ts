export const useImagePath = () => {
  const resolveImagePath = (path: string): string => {
    if (!path) return ''

    // If it's already an absolute URL, return as is
    if (path.startsWith('http')) return path

    // If it's a relative path starting with /, prepend base URL in production
    if (path.startsWith('/')) {
      // Get base URL from runtime config or environment
      const baseURL = process.env.NODE_ENV === 'production' ? '/frontend' : ''
      return `${baseURL}${path}`
    }

    return path
  }

  return {
    resolveImagePath
  }
}
