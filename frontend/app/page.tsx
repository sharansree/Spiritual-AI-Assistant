'use client'
import Link from 'next/link'
import { useAuth } from '@/lib/auth-context'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import styles from './page.module.css'

export default function Home() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) router.push('/ask')
  }, [user, loading, router])

  return (
    <main className={styles.main}>
      <div className={styles.ornament}>❧</div>
      <div className={styles.hero}>
        <p className={styles.eyebrow}>The Pali Canon · Theravāda Teachings</p>
        <h1 className={styles.title}>Sathya</h1>
        <p className={styles.subtitle}>
          Bring any question. Receive guidance grounded in the<br />
          original words of the Buddha, cited to their source.
        </p>
        <div className={styles.actions}>
          <Link href="/auth/register" className="btn-primary">Begin</Link>
          <Link href="/auth/login" className="btn-ghost">Sign in</Link>
        </div>
      </div>

      <hr className="divider" style={{ width: '100%', maxWidth: 480, margin: '0 auto' }} />

      <div className={styles.teachings}>
        <p className={styles.teachingLabel}>From the canon</p>
        <blockquote className={styles.quote}>
          "If you knew what I know about the power of giving, you would not let a single meal
          pass without sharing it in some way."
        </blockquote>
        <p className={styles.quoteSource}>AN 5.35 · Anguttara Nikaya</p>
      </div>

      <div className={styles.features}>
        <div className={styles.feature}>
          <span className={styles.featureGlyph}>⊕</span>
          <p className={styles.featureName}>Semantic search</p>
          <p className={styles.featureDesc}>Your question is matched to the most relevant suttas across the Pali Canon using vector embeddings.</p>
        </div>
        <div className={styles.feature}>
          <span className={styles.featureGlyph}>◎</span>
          <p className={styles.featureName}>Cited sources</p>
          <p className={styles.featureDesc}>Every response shows exactly which teaching it draws from — the collection, book, and sutta number.</p>
        </div>
        <div className={styles.feature}>
          <span className={styles.featureGlyph}>◈</span>
          <p className={styles.featureName}>Personal library</p>
          <p className={styles.featureDesc}>Your questions and the teachings they surfaced are saved to your library to return to.</p>
        </div>
      </div>

      <footer className={styles.footer}>
        <p>Teachings drawn from the Pali Canon · Public domain translations</p>
      </footer>
    </main>
  )
}