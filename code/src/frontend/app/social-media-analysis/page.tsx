"use client"

import { useState , useEffect} from "react"
import Image from "next/image"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog"
import { X } from "lucide-react"
import axios from "axios"

// Updated interface to match the API response
interface Product {
  id: string
  consumer_insights?: Array<{
    insight?: string
    details?: string
    description?: string
  }>
  market_implications?: Array<{
    implication?: string
    opportunity?: string
    description?: string
  }>
  recommendations?: Array<{
    recommendation?: string
    rationale?: string
    description?: string
  }>
  trend_summary?: string
  instagram_ad?: string
  linkedin_ad?: string
  meta_ad?: string
  generated_at?: string
}
interface AdResponse {
  type: string
  content: string
  imageUrl: string
}
// Mock product data
const products = [
  {
    id: 1,
    name: "Credit Card",
    description: "Enterprise-grade business intelligence platform",
    insights:
      "The conversations highlight several key trends: \n(1) Increased interest in credit card rewards, particularly for travel optimization.\n (2) Emphasis on using credit cards for building credit scores, especially among first-time users and students.\n (3) Significant engagement with debt management services and credit counseling for high-interest debt reduction.\n (4) Focus on user experience, particularly related to customer service and ease of application",
    recommendations:
      "Focus marketing efforts on LinkedIn and Meta for this product. Target decision-makers in enterprise companies.",
    opportunity: "Expanding reach to mid-market companies could increase market share by an estimated 15%.",
  },
  {
    id: 2,
    name: "Home Loan",
    description: "Consumer-facing mobile application",
    insights:
      "Several key trends are emerging from social media conversations about home loans: the persistent interest in low down payment options (FHA loans), the exploration of alternative financing like HELOCs and construction loans, the perceived value of mortgage brokers in securing better rates, and the importance of clear communication and support from loan officers. First-time homebuyers are actively seeking advice and sharing their experiences, both positive and negative",
    recommendations: "Increase Instagram ad spend and develop more visual content. Consider influencer partnerships.",
    opportunity: "Expanding to TikTok could capture additional market share in the 18-24 demographic.",
  },
  {
    id: 3,
    name: "Mortgage",
    description: "SaaS solution for small businesses",
    insights: "Product Gamma has moderate performance across all platforms, with slightly better results on LinkedIn.",
    recommendations:
      "Refine messaging to better highlight small business benefits. Test different ad creatives on Meta.",
    opportunity: "Creating industry-specific landing pages could improve conversion rates by an estimated 20%.",
  },
  {
    id: 4,
    name: "Auto loan",
    description: "Premium subscription service",
    insights: "Product Delta resonates well with professionals on LinkedIn and has good engagement on Meta.",
    recommendations: "Focus on value proposition in LinkedIn content. Highlight premium features in Meta ads.",
    opportunity: "Developing a referral program could leverage existing customer base for growth.",
  },
]

// Mock ad generation responses
const mockAdResponses = {
  meta: {
    content:
      "Streamline your business operations with our powerful solution. Try Product Alpha today and see how our enterprise-grade platform can transform your data into actionable insights. Start your free trial now!",
    imageUrl: "/creditCard.jpg?height=400&width=400",
  },
  instagram: {
    content:
      "Transform your business with data-driven decisions. Our intuitive platform makes complex analytics simple. #BusinessIntelligence #DataAnalytics #ProductAlpha",
    imageUrl: "/creditCard.jpg?",
  },
  linkedin: {
    content:
      "Empower your team with enterprise-grade analytics. Product Alpha helps businesses like yours make smarter decisions with real-time insights and powerful visualization tools. Join thousands of companies already using our platform to drive growth.",
    imageUrl: "/creditCard.jpg?",
  },
}

export default function SocialMediaAnalysis() {
  const [products, setProducts] = useState<Product[]>([])
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [adType, setAdType] = useState<null | "meta" | "instagram" | "linkedin">(null)
  const [adData, setAdData] = useState<null | { content: string; imageUrl: string }>(null)
  const [isAdModalOpen, setIsAdModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  // Fetch products on component mount
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setIsLoading(true)
        const response = await axios.get('http://127.0.0.1:5000/get-scoialmediainsights')
        
        // Filter out empty products
        const validProducts = response.data.filter((product: Product) => 
          product.consumer_insights?.length || 
          product.market_implications?.length || 
          product.recommendations?.length
        )
        
        setProducts(validProducts)
        // Set first product as default selected product
        if (validProducts.length > 0) {
          setSelectedProduct(validProducts[0])
        }
        setIsLoading(false)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred while fetching products')
        setIsLoading(false)
      }
    }

    fetchProducts()
  }, [])
  // Loading state
  if (isLoading) {
    return <div className="container mx-auto p-4">Loading products...</div>
  }

  // Error state
  if (error) {
    return <div className="container mx-auto p-4 text-red-500">{error}</div>
  }

  // If no products found
  if (products.length === 0) {
    return <div className="container mx-auto p-4">No products found.</div>
  }
  const generateAd = (type: "meta" | "instagram" | "linkedin") => {
    if (type === "meta") {
      setAdData({
        content: selectedProduct?.meta_ad || mockAdResponses.meta.content,
        imageUrl: mockAdResponses.meta.imageUrl,
      })
      setAdType("meta")
      setIsAdModalOpen(true)
    }
    if(type === "instagram") {
      setAdData({
        content: selectedProduct?.instagram_ad || mockAdResponses.instagram.content,
        imageUrl: mockAdResponses.instagram.imageUrl,
      })
      setAdType("instagram")
      setIsAdModalOpen(true)
    }
    if(type === "linkedin") {
      setAdData({
        content: selectedProduct?.linkedin_ad || mockAdResponses.linkedin.content,
        imageUrl: mockAdResponses.linkedin.imageUrl,
      })
      setAdType("linkedin")
      setIsAdModalOpen(true)
    } 
  }

  return (
    <div className="container mx-auto p-4 md:p-6">
      <h1 className="text-3xl font-bold mb-6">Social Media Analysis</h1>

      <div className="space-y-8">
        {products.map((product) => (
          <Card key={product.id} className="w-full">
            <CardHeader>
              <CardTitle>{product.id}</CardTitle>
              {product.trend_summary && (
                <CardDescription>{product.trend_summary}</CardDescription>
              )}
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="insights" className="w-full">
                <TabsList className="mb-4">
                  <TabsTrigger value="insights">Insights</TabsTrigger>
                  <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
                  <TabsTrigger value="market_implications">Market Implications</TabsTrigger>
                </TabsList>
                
                <TabsContent value="insights" className="p-4 bg-muted rounded-md">
                  {product.consumer_insights && product.consumer_insights.length > 0 ? (
                    <ul className="list-disc pl-5 space-y-2">
                      {product.consumer_insights.map((insight, index) => (
                        <li key={index}>
                          <strong>{insight.insight || 'Insight'}:</strong> 
                          {insight.details || insight.description || 'No details available'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No insights available</p>
                  )}
                </TabsContent>
                
                <TabsContent value="recommendations" className="p-4 bg-muted rounded-md">
                  {product.recommendations && product.recommendations.length > 0 ? (
                    <ul className="list-disc pl-5 space-y-2">
                      {product.recommendations.map((rec, index) => (
                        <li key={index}>
                          <strong>{rec.recommendation || 'Recommendation'}:</strong> 
                          {rec.rationale || rec.description || 'No details available'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No recommendations available</p>
                  )}
                </TabsContent>
                
                <TabsContent value="market_implications" className="p-4 bg-muted rounded-md">
                  {product.market_implications && product.market_implications.length > 0 ? (
                    <ul className="list-disc pl-5 space-y-2">
                      {product.market_implications.map((imp, index) => (
                        <li key={index}>
                          <strong>{imp.implication || 'Implication'}:</strong> 
                          {imp.opportunity || imp.description || 'No details available'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No market implications available</p>
                  )}
                </TabsContent>
              </Tabs>


              <div className="flex flex-wrap gap-3 mt-6">
                <Button
                  variant="outline"
                  onClick={() => {
                    setSelectedProduct(product)
                    generateAd("meta")
                  }}
                >
                  Generate Meta Ad
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setSelectedProduct(product)
                    generateAd("instagram")
                  }}
                >
                  Generate Instagram Ad
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setSelectedProduct(product)
                    generateAd("linkedin")
                  }}
                >
                  Generate LinkedIn Ad
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Ad Preview Modal */}
      <Dialog open={isAdModalOpen} onOpenChange={setIsAdModalOpen}>
      
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {adType === "meta" ? "Meta Ad" : adType === "instagram" ? "Instagram Ad" : "LinkedIn Ad"} for{" "}
              {selectedProduct?.id}
            </DialogTitle>
          </DialogHeader>
          <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </DialogClose>

          {adData && (
            <div className="space-y-4">
              {adType === "instagram" ? (
                <div className="border rounded-lg overflow-hidden max-w-md mx-auto">
                  <div className="bg-white p-2 flex items-center gap-2 border-b">
                    <div className="w-8 h-8 rounded-full bg-gray-200"></div>
                    <div className="text-sm font-medium">your_company</div>
                  </div>
                  <div className="aspect-square relative">
                    <Image src={adData.imageUrl || "/placeholder.svg"} alt="Ad preview" fill className="object-cover" />
                  </div>
                  <div className="p-3 bg-white">
                    <div className="flex gap-3 mb-2">
                      <div className="w-6 h-6 flex items-center justify-center">❤️</div>
                      <div className="w-6 h-6 flex items-center justify-center">💬</div>
                      <div className="w-6 h-6 flex items-center justify-center">📤</div>
                    </div>
                    <div className="text-sm">
                      <span className="font-bold">your_company</span> {adData.content}
                    </div>
                  </div>
                </div>
              ) : adType === "meta" ? (
                <div className="border rounded-lg overflow-hidden max-w-md mx-auto">
                  <div className="bg-white p-3 flex items-start gap-2">
                    <div className="w-10 h-10 rounded-full bg-gray-200 flex-shrink-0"></div>
                    <div>
                      <div className="font-medium">Your Company</div>
                      <div className="text-xs text-gray-500">
                        Sponsored · <span>👥</span>
                      </div>
                    </div>
                  </div>
                  <div className="p-3 bg-white text-sm">{adData.content}</div>
                  <div className="aspect-video relative">
                    <Image src={adData.imageUrl || "/placeholder.svg"} alt="Ad preview" fill className="object-cover" />
                  </div>
                  <div className="bg-white p-2 flex justify-between border-t">
                    <div className="flex gap-2">
                      <div className="text-sm">👍 Like</div>
                      <div className="text-sm">💬 Comment</div>
                    </div>
                    <div className="text-sm">↗️ Share</div>
                  </div>
                </div>
              ) : (
                <div className="border rounded-lg overflow-hidden max-w-md mx-auto">
                  <div className="bg-white p-3 flex items-start gap-2 border-b">
                    <div className="w-12 h-12 rounded-full bg-gray-200 flex-shrink-0"></div>
                    <div>
                      <div className="font-medium">Your Company</div>
                      <div className="text-xs text-gray-500">Sponsored · 1d</div>
                    </div>
                  </div>
                  <div className="p-4 bg-white text-sm">{adData.content}</div>
                  <div className="aspect-video relative">
                    <Image src={adData.imageUrl || "/placeholder.svg"} alt="Ad preview" fill className="object-cover" />
                  </div>
                  <div className="bg-white p-3 flex gap-4 border-t">
                    <div className="text-sm font-medium">👍 Like</div>
                    <div className="text-sm font-medium">💬 Comment</div>
                    <div className="text-sm font-medium">↗️ Share</div>
                  </div>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

