import { fetchCompanies } from "@/lib/api"
import { CompanyCard } from "@/components/CompanyCard"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default async function Home({ searchParams }: { searchParams: { q?: string, sector?: string, stage?: string } }) {
  const companies = await fetchCompanies(searchParams);

  return (
    <div className="container mx-auto px-4 py-8 flex flex-col md:flex-row gap-8">
      <aside className="w-full md:w-64 shrink-0 space-y-6">
        <div>
          <h3 className="font-semibold mb-3">Sector</h3>
          <div className="space-y-2 text-sm">
            <p className="cursor-pointer hover:underline text-muted-foreground">fintech</p>
            <p className="cursor-pointer hover:underline text-muted-foreground">saas</p>
            <p className="cursor-pointer hover:underline text-muted-foreground">ai</p>
            <p className="cursor-pointer hover:underline text-muted-foreground">marketplace</p>
          </div>
        </div>
        <div>
          <h3 className="font-semibold mb-3">Stage</h3>
          <div className="space-y-2 text-sm">
            <p className="cursor-pointer hover:underline text-muted-foreground">seed</p>
            <p className="cursor-pointer hover:underline text-muted-foreground">series-a</p>
            <p className="cursor-pointer hover:underline text-muted-foreground">ipo</p>
          </div>
        </div>
      </aside>

      <div className="flex-1 space-y-6">
        <form className="flex gap-2">
          <Input 
            name="q" 
            placeholder="Search startups by name or description..." 
            defaultValue={searchParams.q}
            className="max-w-xl bg-background"
          />
          <Button type="submit">Search</Button>
        </form>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company: any) => (
            <CompanyCard key={company.id} company={company} />
          ))}
          {companies.length === 0 && (
            <p className="text-muted-foreground py-10">No startups found matching your criteria.</p>
          )}
        </div>
      </div>
    </div>
  )
}
