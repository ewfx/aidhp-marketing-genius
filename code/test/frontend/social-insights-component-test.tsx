import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import axios from 'axios'
import SocialMediaAnalysis from './page'

// Mock axios
jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

// Mock Lucide icons
jest.mock('lucide-react', () => ({
  X: () => <div data-testid="x-icon" />
}))

// Mock Next.js Image component
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props: any) => {
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...props} alt={props.alt} />
  }
}))

// Mock UI components
jest.mock('@/components/ui/tabs', () => ({
  Tabs: ({ children }) => <div data-testid="tabs">{children}</div>,
  TabsContent: ({ children }) => <div>{children}</div>,
  TabsList: ({ children }) => <div>{children}</div>,
  TabsTrigger: ({ children, value }) => <button data-value={value}>{children}</button>
}))

jest.mock('@/components/ui/card', () => ({
  Card: ({ children }) => <div data-testid="card">{children}</div>,
  CardHeader: ({ children }) => <div>{children}</div>,
  CardTitle: ({ children }) => <h3>{children}</h3>,
  CardContent: ({ children }) => <div>{children}</div>,
  CardDescription: ({ children }) => <p>{children}</p>
}))

const mockProducts = [
  {
    id: '1',
    consumer_insights: [{ insight: 'Test Insight', details: 'Insight Details' }],
    market_implications: [{ implication: 'Test Implication', opportunity: 'Opportunity Details' }],
    recommendations: [{ recommendation: 'Test Recommendation', rationale: 'Rationale Details' }],
    meta_ad: 'Meta Ad Content',
    instagram_ad: 'Instagram Ad Content',
    linkedin_ad: 'LinkedIn Ad Content'
  }
]

describe('SocialMediaAnalysis Component', () => {
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks()
  })

  test('fetches and renders products', async () => {
    // Mock successful API response
    mockedAxios.get.mockResolvedValue({ data: mockProducts })

    render(<SocialMediaAnalysis />)

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument()
    })
  })

  test('handles loading state', () => {
    // Mock pending API response
    mockedAxios.get.mockImplementation(() => new Promise(() => {}))

    render(<SocialMediaAnalysis />)

    expect(screen.getByText('Loading products...')).toBeInTheDocument()
  })

  test('handles error state', async () => {
    // Mock error response
    mockedAxios.get.mockRejectedValue(new Error('Fetch failed'))

    render(<SocialMediaAnalysis />)

    await waitFor(() => {
      expect(screen.getByText(/An error occurred/)).toBeInTheDocument()
    })
  })

  test('opens ad generation modal', async () => {
    // Mock successful API response
    mockedAxios.get.mockResolvedValue({ data: mockProducts })

    render(<SocialMediaAnalysis />)

    // Wait for products to load
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument()
    })

    // Click Meta Ad button
    const metaAdButton = screen.getByText('Generate Meta Ad')
    fireEvent.click(metaAdButton)

    // Check if ad modal opens
    await waitFor(() => {
      expect(screen.getByText('Meta Ad for 1')).toBeInTheDocument()
    })
  })

  test('switches between tabs', async () => {
    // Mock successful API response
    mockedAxios.get.mockResolvedValue({ data: mockProducts })

    render(<SocialMediaAnalysis />)

    // Wait for products to load
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument()
    })

    // Check initial insights tab
    expect(screen.getByText('Test Insight')).toBeInTheDocument()

    // Switch to recommendations tab
    const recommendationsTab = screen.getByText('Recommendations')
    fireEvent.click(recommendationsTab)

    // Check recommendations content
    expect(screen.getByText('Test Recommendation')).toBeInTheDocument()

    // Switch to market implications tab
    const marketImplicationsTab = screen.getByText('Market Implications')
    fireEvent.click(marketImplicationsTab)

    // Check market implications content
    expect(screen.getByText('Test Implication')).toBeInTheDocument()
  })

  test('generates different ad types', async () => {
    // Mock successful API response
    mockedAxios.get.mockResolvedValue({ data: mockProducts })

    render(<SocialMediaAnalysis />)

    // Wait for products to load
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument()
    })

    // Test Meta Ad
    const metaAdButton = screen.getByText('Generate Meta Ad')
    fireEvent.click(metaAdButton)
    await waitFor(() => {
      expect(screen.getByText('Meta Ad for 1')).toBeInTheDocument()
    })

    // Close modal
    const closeButton = screen.getByTestId('x-icon')
    fireEvent.click(closeButton)

    // Test Instagram Ad
    const instagramAdButton = screen.getByText('Generate Instagram Ad')
    fireEvent.click(instagramAdButton)
    await waitFor(() => {
      expect(screen.getByText('Instagram Ad for 1')).toBeInTheDocument()
    })

    // Close modal
    fireEvent.click(screen.getByTestId('x-icon'))

    // Test LinkedIn Ad
    const linkedinAdButton = screen.getByText('Generate LinkedIn Ad')
    fireEvent.click(linkedinAdButton)
    await waitFor(() => {
      expect(screen.getByText('LinkedIn Ad for 1')).toBeInTheDocument()
    })
  })
})