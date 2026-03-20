import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default async function CompanyPage({ params }: { params: { slug: string } }) {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
  const res = await fetch(`${API_BASE_URL}/companies/${params.slug}`, { cache: 'no-store' });
  
  if (!res.ok) {
    return <div className="p-8 text-center text-muted-foreground">Company not found.</div>;
  }
  
  const company = await res.json();
  
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Card className="bg-card">
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-4xl font-bold">{company.name}</CardTitle>
              <div className="mt-4 flex gap-2">
                {company.sector && <Badge variant="secondary">{company.sector}</Badge>}
                {company.stage && <Badge variant="outline">{company.stage}</Badge>}
                <Badge variant={company.status === 'active' ? 'default' : 'destructive'}>{company.status}</Badge>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {company.description && (
            <div>
              <h3 className="text-xl font-semibold mb-2">About</h3>
              <p className="text-muted-foreground">{company.description}</p>
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-4 border-t pt-6">
            <div>
              <span className="font-semibold text-sm text-foreground mb-1 block">Website</span>
              <a href={company.website} target="_blank" className="text-primary hover:underline">{company.website || 'N/A'}</a>
            </div>
            {company.founded_year && (
              <div>
                <span className="font-semibold text-sm text-foreground mb-1 block">Founded</span>
                <span className="text-muted-foreground">{company.founded_year}</span>
              </div>
            )}
            {company.location && (
              <div>
                <span className="font-semibold text-sm text-foreground mb-1 block">Location</span>
                <span className="text-muted-foreground">{company.location}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
