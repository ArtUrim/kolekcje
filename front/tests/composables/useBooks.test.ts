import { describe, it, expect, beforeEach, vi } from 'vitest'
import { ref, nextTick } from 'vue'
import { useBooks } from '~/composables/useBooks'

// Mock the useAPI composable
vi.mock('~/composables/useAPI', () => ({
  useAPI: vi.fn()
}))

// Mock useI18n
vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: (key: string) => key
  })
}))

// Mock onUnmounted
vi.mock('vue', async () => {
  const actual = await vi.importActual('vue')
  return {
    ...actual,
    onUnmounted: vi.fn()
  }
})

describe('useBooks', () => {
  let mockUseAPI: any
  
  beforeEach(() => {
    vi.clearAllMocks()
    mockUseAPI = require('~/composables/useAPI').useAPI
  })

  describe('fetchBooks', () => {
    it('should fetch books from /books endpoint', async () => {
      const mockData = {
        books: [
          { id: 1, title: 'Book 1' },
          { id: 2, title: 'Book 2' }
        ],
        count: 2
      }
      
      mockUseAPI.mockResolvedValue(mockData)
      
      const { fetchBooks, items, totalItems } = useBooks()
      
      await fetchBooks({ page: 1, itemsPerPage: 10 })
      
      expect(mockUseAPI).toHaveBeenCalledWith('/books?page=1&itemsPerPage=10')
      expect(items.value).toHaveLength(2)
      expect(totalItems.value).toBe(2)
    })

    it('should handle query parameters correctly', async () => {
      const mockData = {
        books: [{ id: 1, title: 'Test Book' }],
        count: 1
      }
      
      mockUseAPI.mockResolvedValue(mockData)
      
      const { fetchBooks } = useBooks()
      
      await fetchBooks({ 
        title: 'Test',
        author: 'Author Name',
        isbn: '1234567890',
        page: 1,
        itemsPerPage: 20
      })
      
      const callArgs = mockUseAPI.mock.calls[0][0]
      expect(callArgs).toContain('/books?')
      expect(callArgs).toContain('title=Test')
      expect(callArgs).toContain('author=Author%20Name')
      expect(callArgs).toContain('isbn=1234567890')
      expect(callArgs).toContain('page=1')
      expect(callArgs).toContain('itemsPerPage=20')
    })

    it('should handle empty response gracefully', async () => {
      mockUseAPI.mockResolvedValue({ books: [], count: 0 })
      
      const { fetchBooks, items, totalItems } = useBooks()
      
      await fetchBooks({ page: 1 })
      
      expect(items.value).toHaveLength(0)
      expect(totalItems.value).toBe(0)
    })

    it('should deduplicate books by id', async () => {
      const mockData = {
        books: [
          { id: 1, title: 'Book 1' },
          { id: 1, title: 'Book 1 Duplicate' },
          { id: 2, title: 'Book 2' }
        ],
        count: 3
      }
      
      mockUseAPI.mockResolvedValue(mockData)
      
      const { fetchBooks, items } = useBooks()
      
      await fetchBooks({ page: 1 })
      
      expect(items.value).toHaveLength(2)
      expect(items.value[0].id).toBe(1)
      expect(items.value[1].id).toBe(2)
    })

    it('should handle error and schedule retry', async () => {
      vi.useFakeTimers()
      mockUseAPI.mockRejectedValue(new Error('Network error'))
      
      const { fetchBooks, isRetrying } = useBooks()
      
      await fetchBooks({ page: 1 })
      
      // Should be retrying after error
      expect(isRetrying.value).toBe(true)
      
      vi.useRealTimers()
    })

    it('should update loading state correctly', async () => {
      const mockData = { books: [], count: 0 }
      mockUseAPI.mockImplementation(() => Promise.resolve(mockData))
      
      const { fetchBooks, loading } = useBooks()
      
      expect(loading.value).toBe(false)
      
      const fetchPromise = fetchBooks({ page: 1 })
      expect(loading.value).toBe(true)
      
      await fetchPromise
      expect(loading.value).toBe(false)
    })
  })

  describe('headers', () => {
    it('should return correct column headers', () => {
      const { headers } = useBooks()
      
      expect(headers.value).toHaveLength(5)
      expect(headers.value.map(h => h.key)).toEqual([
        'title',
        'authors',
        'publisher',
        'release_date',
        'series_name'
      ])
    })
  })
})
