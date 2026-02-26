export const useImagePath = () => {
  const resolveImagePath = (path: string): string => {
    if (!path) return ''
    return path
  }
  return {
    resolveImagePath
  }
}
