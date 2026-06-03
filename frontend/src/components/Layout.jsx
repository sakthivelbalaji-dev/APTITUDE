export function Logo({ className = 'h-8' }) {
  return (
    <img
      src="/capgemini-logo.svg"
      alt="Capgemini"
      className={className}
    />
  )
}

export function Footer() {
  return (
    <footer className="mt-auto py-6 text-center text-sm text-slate-500 border-t border-capgemini-border">
      © 2026 Capgemini Assessment Platform. All Rights Reserved.
    </footer>
  )
}

export function PageLayout({ children, showFooter = true }) {
  return (
    <div className="min-h-screen flex flex-col bg-capgemini-dark">
      <header className="px-4 py-4 border-b border-capgemini-border glass">
        <div className="max-w-4xl mx-auto flex items-center justify-center">
          <Logo className="h-9 animate-float-3d" />
        </div>
      </header>
      <main className="flex-1 px-4 py-6 max-w-4xl mx-auto w-full animate-slide-in-3d">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  )
}

export function Button({ children, variant = 'primary', className = '', ...props }) {
  const base = 'w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed btn-3d'
  const variants = {
    primary: 'gradient-bg text-white',
    secondary: 'glass border border-capgemini-border text-slate-200 hover:border-capgemini-light',
    danger: 'bg-gradient-to-r from-red-600 to-red-500 text-white',
  }
  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  )
}

export function Input({ label, ...props }) {
  return (
    <div className="mb-4">
      {label && <label className="block text-sm text-slate-400 mb-2">{label}</label>}
      <input
        className="w-full px-4 py-3 rounded-xl glass border border-capgemini-border text-white placeholder-slate-500 focus:outline-none focus:border-capgemini-light focus:ring-1 focus:ring-capgemini-light transition input-3d"
        {...props}
      />
    </div>
  )
}

export function Card({ children, className = '' }) {
  return (
    <div className={`glass border border-capgemini-border rounded-2xl p-6 shadow-xl card-3d animate-glow ${className}`}>
      {children}
    </div>
  )
}
