import { Outlet, Navigate, NavLink } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { LogOut, MessageSquare, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'

const isDev = import.meta.env.VITE_SUPABASE_URL === 'https://placeholder.supabase.co'

export function Layout() {
  const { user, loading, signOut } = useAuth()

  if (loading && !isDev) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!user && !isDev) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="container mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <h1 className="text-lg font-semibold">Agentic RAG</h1>
            <nav className="flex items-center gap-1">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-1.5 rounded-md text-sm transition-colors ${
                    isActive
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`
                }
              >
                <MessageSquare className="h-4 w-4" />
                Chat
              </NavLink>
              <NavLink
                to="/documents"
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-1.5 rounded-md text-sm transition-colors ${
                    isActive
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`
                }
              >
                <FileText className="h-4 w-4" />
                Documents
              </NavLink>
            </nav>
          </div>
          <div className="flex items-center gap-2">
            {isDev && <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">Dev Mode</span>}
            {!isDev && (
              <Button variant="ghost" size="icon" onClick={signOut}>
                <LogOut className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      </header>
      <main className="flex-1 container mx-auto px-4">
        <Outlet />
      </main>
    </div>
  )
}
