"use client"

import { useState } from "react"
import Link from "next/link"
import { BarChart3, X } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogClose,
} from "@/components/ui/dialog"

// Mock API data
const painPointsData = {
  title: "Company A Pain Point Analysis",
  description: "Comprehensive analysis of pain points identified through customer feedback and market research.",
  points: [
    {
      id: 1,
      title: "Customer Acquisition",
      description:
        "High cost of customer acquisition through traditional channels. Digital marketing efforts are not optimized for conversion.",
      impact: "High",
      recommendation: "Implement targeted digital marketing campaigns with improved analytics tracking.",
    },
    {
      id: 2,
      title: "User Experience",
      description:
        "Customer feedback indicates frustration with the product onboarding process and interface complexity.",
      impact: "Medium",
      recommendation: "Redesign onboarding flow and simplify UI based on user testing.",
    },
    {
      id: 3,
      title: "Customer Retention",
      description: "Higher than industry average churn rate, particularly after the first 3 months of usage.",
      impact: "Critical",
      recommendation:
        "Develop a robust customer success program and implement early warning systems for at-risk customers.",
    },
  ],
}

export default function Dashboard() {
  const [isPainPointsOpen, setIsPainPointsOpen] = useState(false)

  return (
    <div className="container mx-auto p-4 md:p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            Export
          </Button>
          <Button size="sm">Refresh Data</Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader>
            <CardTitle>Company A Pain Point Analysis</CardTitle>
            <CardDescription>Detailed analysis of customer pain points and recommendations</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              This analysis identifies key areas where customers experience friction and provides actionable
              recommendations.
            </p>
            <Button onClick={() => setIsPainPointsOpen(true)}>View Analysis</Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardHeader>
            <CardTitle>Social Media Analysis</CardTitle>
            <CardDescription>Performance metrics and insights across social platforms</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Comprehensive analysis of social media performance, engagement metrics, and content effectiveness.
            </p>
            <Button asChild>
              <Link href="/social-media-analysis">
                <BarChart3 className="mr-2 h-4 w-4" />
                View Analysis
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Pain Points Analysis Modal */}
      <Dialog open={isPainPointsOpen} onOpenChange={setIsPainPointsOpen}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{painPointsData.title}</DialogTitle>
            <DialogDescription>{painPointsData.description}</DialogDescription>
          </DialogHeader>
          <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </DialogClose>

          <div className="space-y-6">
            {painPointsData.points.map((point) => (
              <div key={point.id} className="border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-lg">{point.title}</h3>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      point.impact === "Critical"
                        ? "bg-red-100 text-red-800"
                        : point.impact === "High"
                          ? "bg-amber-100 text-amber-800"
                          : "bg-blue-100 text-blue-800"
                    }`}
                  >
                    {point.impact} Impact
                  </span>
                </div>
                <p className="text-muted-foreground mb-2">{point.description}</p>
                <div className="bg-muted p-3 rounded-md">
                  <span className="font-medium">Recommendation:</span> {point.recommendation}
                </div>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

