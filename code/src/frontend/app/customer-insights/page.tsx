"use client"

import { useState } from "react"
import { Mail, MessageSquare, Bell, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog"

// Mock customer data
const customers = [
  {
    id: 1,
    name: "Jane Cooper",
    email: "jane.cooper@example.com",
    company: "Acme Inc",
    status: "Active",
    lastPurchase: "2023-12-15",
    totalSpent: "$12,500",
    insight: "Jane is highly engaged with our premium features.",
    recommendation: "Offer Jane early access to our new AI-powered tools.",
  },
  {
    id: 2,
    name: "Wade Warren",
    email: "wade.warren@example.com",
    company: "Globex Corp",
    status: "Active",
    lastPurchase: "2024-01-20",
    totalSpent: "$8,200",
    insight: "Wade frequently uses our mobile app.",
    recommendation: "Promote our mobile-exclusive deals to Wade.",
  },
  {
    id: 3,
    name: "Esther Howard",
    email: "esther.howard@example.com",
    company: "Soylent Corp",
    status: "Inactive",
    lastPurchase: "2023-10-05",
    totalSpent: "$5,100",
    insight: "Esther hasn't logged in for several months.",
    recommendation: "Send Esther a personalized re-engagement email.",
  },
  {
    id: 4,
    name: "Cameron Williamson",
    email: "cameron.williamson@example.com",
    company: "Initech",
    status: "Active",
    lastPurchase: "2024-02-10",
    totalSpent: "$15,800",
    insight: "Cameron is a power user of our API.",
    recommendation: "Invite Cameron to our developer conference.",
  },
  {
    id: 5,
    name: "Brooklyn Simmons",
    email: "brooklyn.simmons@example.com",
    company: "Umbrella Corp",
    status: "Active",
    lastPurchase: "2024-01-05",
    totalSpent: "$9,300",
    insight: "Brooklyn often provides valuable feedback.",
    recommendation: "Nominate Brooklyn for our customer advisory board.",
  },
]

// Mock content generation responses
const mockContentResponses = {
  email: `<p>Dear [Customer Name],</p>
<p>I hope this email finds you well. We wanted to take a moment to thank you for your continued partnership with us.</p>
<p>We've noticed that you've been using our [Product Name] solution, and we wanted to check in to see how it's working for you. Our records show that you might benefit from some of the new features we've recently added:</p>
<ul>
  <li>Advanced reporting capabilities</li>
  <li>Improved integration with third-party tools</li>
  <li>Enhanced security features</li>
</ul>
<p>Would you be interested in scheduling a brief call to discuss how these features could help streamline your operations further?</p>
<p>Best regards,<br>
Your Account Manager<br>
Company Name</p>`,

  pushNotification:
    "New feature alert! We've just launched our advanced reporting dashboard. Check it out now to gain deeper insights into your business performance.",

  sms: "Hi [Customer Name], thank you for your recent purchase! Use code THANKS10 for 10% off your next order. Valid for 7 days. Reply STOP to opt out.",
}

type ContentType = "email" | "pushNotification" | "sms"

export default function CustomerInsights() {
  const [selectedCustomer, setSelectedCustomer] = useState<(typeof customers)[0] | null>(null)
  const [contentType, setContentType] = useState<ContentType | null>(null)
  const [content, setContent] = useState("")
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [expandedContent, setExpandedContent] = useState<{
    type: "insight" | "recommendation"
    content: string
  } | null>(null)

  const generateContent = (customer: (typeof customers)[0], type: ContentType) => {
    setSelectedCustomer(customer)
    setContentType(type)

    // Simulate API call
    setTimeout(() => {
      let generatedContent = mockContentResponses[type]

      // Replace placeholders with customer data
      if (type === "email" || type === "sms") {
        generatedContent = generatedContent.replace("[Customer Name]", customer.name)
      }

      setContent(generatedContent)
      setIsModalOpen(true)
    }, 500)
  }

  return (
    <div className="container mx-auto p-4 md:p-6">
      <h1 className="text-3xl font-bold mb-6">Customer Insights</h1>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Purchase</TableHead>
              <TableHead>Total Spent</TableHead>
              <TableHead>Insight</TableHead>
              <TableHead>Recommendation</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {customers.map((customer) => (
              <TableRow key={customer.id}>
                <TableCell className="font-medium">{customer.name}</TableCell>
                <TableCell>{customer.email}</TableCell>
                <TableCell>{customer.company}</TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      customer.status === "Active" ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {customer.status}
                  </span>
                </TableCell>
                <TableCell>{customer.lastPurchase}</TableCell>
                <TableCell>{customer.totalSpent}</TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    className="p-0 h-auto font-normal text-left justify-start hover:bg-transparent hover:underline"
                    onClick={() => setExpandedContent({ type: "insight", content: customer.insight })}
                  >
                    {customer.insight.length > 40 ? `${customer.insight.substring(0, 40)}...` : customer.insight}
                  </Button>
                </TableCell>
                <TableCell>
                  <Button
                    variant="ghost"
                    className="p-0 h-auto font-normal text-left justify-start hover:bg-transparent hover:underline"
                    onClick={() => setExpandedContent({ type: "recommendation", content: customer.recommendation })}
                  >
                    {customer.recommendation.length > 40
                      ? `${customer.recommendation.substring(0, 40)}...`
                      : customer.recommendation}
                  </Button>
                </TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => generateContent(customer, "email")}>
                      <Mail className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => generateContent(customer, "pushNotification")}>
                      <Bell className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => generateContent(customer, "sms")}>
                      <MessageSquare className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Content Modal */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {contentType === "email"
                ? "Email Template"
                : contentType === "pushNotification"
                  ? "Push Notification"
                  : "SMS Message"}{" "}
              for {selectedCustomer?.name}
            </DialogTitle>
          </DialogHeader>
          <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </DialogClose>

          <div className="space-y-4">
            {contentType === "email" ? (
              <div className="border rounded-lg p-4 bg-white">
                <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: content }}></div>
              </div>
            ) : contentType === "pushNotification" ? (
              <div className="border rounded-lg overflow-hidden max-w-md mx-auto">
                <div className="bg-slate-800 text-white p-3">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-6 h-6 rounded bg-primary"></div>
                    <div className="text-sm font-medium">Your App</div>
                    <div className="text-xs text-slate-300 ml-auto">now</div>
                  </div>
                  <div className="text-sm">{content}</div>
                </div>
              </div>
            ) : (
              <div className="border rounded-lg overflow-hidden max-w-md mx-auto">
                <div className="bg-slate-100 p-4">
                  <div className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="text-sm">{content}</div>
                    <div className="text-xs text-right text-slate-500 mt-1">Delivered</div>
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button>
                Send {contentType === "email" ? "Email" : contentType === "pushNotification" ? "Notification" : "SMS"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
      {/* Expanded Content Modal */}
      <Dialog open={expandedContent !== null} onOpenChange={(open) => !open && setExpandedContent(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{expandedContent?.type === "insight" ? "Customer Insight" : "Recommendation"}</DialogTitle>
          </DialogHeader>
          <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </DialogClose>

          <div className="p-4 bg-muted rounded-md">{expandedContent?.content}</div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

