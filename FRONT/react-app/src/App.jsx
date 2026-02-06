import Layout from "./components//Layout"
import SideBarLeft from "./components/SideBarLeft"
import AnimatedAiMain from "./components/AnimatedAiMain"
import TextRenderer from "./components/TextRenderer"
import Footer from "./components/Footer"

function App() {
  return (
    <Layout
      left={<SideBarLeft />}
      center={<AnimatedAiMain />}
      right={<TextRenderer />}
      footer={<Footer />}
    />
  )
}

export default App
