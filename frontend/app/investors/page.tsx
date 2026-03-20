import { fetchInvestors } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default async function InvestorsPage() {
  const investors = await fetchInvestors();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Investors & Accelerators</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {investors.map((inv: any) => (
          <Card key={inv.id} className="bg-card">
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                {inv.name}
              </CardTitle>
              <CardDescription>{inv.location || "Global"}</CardDescription>
            </CardHeader>
            <CardContent>
              <Badge variant="secondary">{inv.type}</Badge>
              <div className="text-sm text-muted-foreground mt-4">
                <a href={inv.portfolio_url} target="_blank" className="hover:underline">View Source Portfolio</a>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
