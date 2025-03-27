import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import CustomerInsights from '../../src/frontend/app/customer-insights/page'


// Mock Lucide icons to avoid import issues
jest.mock('lucide-react', () => ({
  Mail: () => <div data-testid="mail-icon" />,
  MessageSquare: () => <div data-testid="message-square-icon" />,
  Bell: () => <div data-testid="bell-icon" />,
  X: () => <div data-testid="x-icon" />
}))

// Mock UI components to simplify testing
jest.mock('@/components/ui/button', () => ({
  Button: ({ children, ...props }) => <button {...props}>{children}</button>
}))

jest.mock('@/components/ui/table', () => ({
  Table: ({ children }) => <table>{children}</table>,
  TableBody: ({ children }) => <tbody>{children}</tbody>,
  TableHead: ({ children }) => <thead>{children}</thead>,
  TableHeader: ({ children }) => <thead>{children}</thead>,
  TableRow: ({ children }) => <tr>{children}</tr>,
  TableCell: ({ children }) => <td>{children}</td>
}))

jest.mock('@/components/ui/dialog', () => ({
  Dialog: ({ children, open, onOpenChange }) => 
    open ? <div data-testid="dialog">{children}</div> : null,
  DialogContent: ({ children }) => <div data-testid="dialog-content">{children}</div>,
  DialogHeader: ({ children }) => <div>{children}</div>,
  DialogTitle: ({ children }) => <h2>{children}</h2>,
  DialogClose: ({ children }) => <button>{children}</button>
}))

describe('CustomerInsights Component', () => {
  beforeEach(() => {
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  test('renders customer insights table', () => {
    render(<CustomerInsights />)
    
    // Check table headers
    expect(screen.getByText('Name')).toBeInTheDocument()
    expect(screen.getByText('Email')).toBeInTheDocument()
    expect(screen.getByText('Company')).toBeInTheDocument()
    
    // Check some customer names
    expect(screen.getByText('Jane Cooper')).toBeInTheDocument()
    expect(screen.getByText('Wade Warren')).toBeInTheDocument()
  })

  test('opens insight modal when insight button is clicked', () => {
    render(<CustomerInsights />)
    
    const insightButtons = screen.getAllByRole('button', { name: /\.{3}/ })
    fireEvent.click(insightButtons[0])
    
    expect(screen.getByTestId('dialog')).toBeInTheDocument()
    expect(screen.getByText(/Jane is highly engaged/)).toBeInTheDocument()
  })

  test('generates content for customer', async () => {
    render(<CustomerInsights />)
    
    const emailButtons = screen.getAllByTestId('mail-icon')
    fireEvent.click(emailButtons[0])
    
    // Simulate API call
    jest.advanceTimersByTime(500)
    
    await waitFor(() => {
      expect(screen.getByTestId('dialog')).toBeInTheDocument()
      expect(screen.getByText(/Dear Jane Cooper/)).toBeInTheDocument()
    })
  })

  test('closes modals', () => {
    render(<CustomerInsights />)
    
    // Open insight modal
    const insightButtons = screen.getAllByRole('button', { name: /\.{3}/ })
    fireEvent.click(insightButtons[0])
    
    // Close modal
    const closeButtons = screen.getAllByTestId('x-icon')
    fireEvent.click(closeButtons[0])
    
    // Verify modal is closed (no dialog visible)
    expect(screen.queryByTestId('dialog')).toBeNull()
  })

  test('renders different action buttons', () => {
    render(<CustomerInsights />)
    
    // Check presence of different action buttons
    expect(screen.getAllByTestId('mail-icon')).toHaveLength(5)
    expect(screen.getAllByTestId('bell-icon')).toHaveLength(5)
    expect(screen.getAllByTestId('message-square-icon')).toHaveLength(5)
  })
})