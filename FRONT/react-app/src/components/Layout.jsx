import './Layout.css'

export default function Layout({ left, center, right, footer }) {
  return (
    <div className="layout">
      <aside>{left}</aside>
      <main>{center}</main>
      <section>{right}</section>
      <footer>{footer}</footer>
    </div>
  )
}