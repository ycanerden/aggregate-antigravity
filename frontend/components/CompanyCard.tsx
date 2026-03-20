import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"

export function CompanyCard({ company }: { company: any }) {
  return (
    <Link href={`/company/${company.slug}`}>
      <Card className="h-full hover:shadow-md transition-shadow cursor-pointer bg-card">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-start">
            <CardTitle>{company.name}</CardTitle>
            {company.logo_url && (
              <img src={company.logo_url} alt={company.name} className="w-8 h-8 rounded-full border" />
            )}
          </div>
          <CardDescription className="line-clamp-2 min-h-[40px]">{company.description || "No description provided."}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 mt-2 flex-wrap">
            {company.sector && <Badge variant="secondary">{company.sector}</Badge>}
            {company.stage && <Badge variant="outline">{company.stage}</Badge>}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
