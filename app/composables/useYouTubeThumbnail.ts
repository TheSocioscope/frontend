/**
 * Composable to extract YouTube video IDs and generate thumbnail URLs
 */
export const useYouTubeThumbnail = () => {
  /**
   * Extract YouTube video ID from various URL formats
   */
  const extractVideoId = (urlOrId: string): string | null => {
    if (!urlOrId) return null

    // If it's already just a video ID (no URL format)
    if (!urlOrId.includes('/') && !urlOrId.includes('http')) {
      return urlOrId
    }

    // Parse as URL
    try {
      const urlObj = new URL(urlOrId)
      let videoId = ''

      // Handle different YouTube URL formats
      if (urlObj.hostname.includes('youtube.com')) {
        videoId = urlObj.searchParams.get('v') || ''
      } else if (urlObj.hostname.includes('youtu.be')) {
        videoId = urlObj.pathname.slice(1)
      }

      return videoId || null
    } catch (e) {
      // If URL parsing fails but looks like a video ID
      if (urlOrId.length === 11 && !urlOrId.includes(' ')) {
        return urlOrId
      }
      return null
    }
  }

  /**
   * Get YouTube thumbnail URL for a video
   * @param urlOrId - YouTube URL or video ID
   * @param quality - Thumbnail quality ('maxresdefault' | 'sddefault' | 'hqdefault' | 'mqdefault' | 'default')
   */
  const getThumbnailUrl = (
    urlOrId: string,
    quality: 'maxresdefault' | 'sddefault' | 'hqdefault' | 'mqdefault' | 'default' = 'hqdefault'
  ): string | null => {
    const videoId = extractVideoId(urlOrId)
    if (!videoId) return null

    return `https://img.youtube.com/vi/${videoId}/${quality}.jpg`
  }

  /**
   * Get YouTube embed URL for a video
   */
  const getEmbedUrl = (urlOrId: string): string | null => {
    const videoId = extractVideoId(urlOrId)
    if (!videoId) return null

    return `https://www.youtube.com/embed/${videoId}`
  }

  return {
    extractVideoId,
    getThumbnailUrl,
    getEmbedUrl
  }
}
