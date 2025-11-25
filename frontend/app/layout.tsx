import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SuperQuantLab 2.0',
  description: 'Crypto Quant Trading Engine & Research Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="border-b border-border bg-card">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <Link href="/" className="text-2xl font-bold">
                SuperQuantLab 2.0
              </Link>
              <div className="flex gap-4">
                <Link href="/" className="hover:text-primary transition-colors">
                  总览 Dashboard
                </Link>
                <Link href="/dashboard" className="hover:text-primary transition-colors">
                  策略表现 Performance
                </Link>
                <Link href="/strategies" className="hover:text-primary transition-colors">
                  策略管理 Strategies
                </Link>
                <Link href="/behavior" className="hover:text-primary transition-colors">
                  行为分析 Behavior
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}

