import { useEffect, ReactElement } from "react";
import { Streamlit, ComponentProps,
  withStreamlitConnection
} from "streamlit-component-lib";
import {ArrowsPointingOutIcon} from '@heroicons/react/24/solid'
import './App.css'
// import Badge from './components/Badge'
// import Button from './components/Button'
import Card from './components/Card'

function App({args}: ComponentProps): ReactElement {
  const {body, title} = args

  useEffect(() => {
    Streamlit.setFrameHeight()
  })

  return (
    <div className="App">
      <section className="card-container">
        <Card
          body={body}
          title={title}
          image="./images/error.jpg"
          btn={{
            text: "Expand",
            href: '#',
            type: 'primary',
            filled: true,
            icon: <ArrowsPointingOutIcon />
          }} />
      </section>
    </div>
  )
}

export default withStreamlitConnection(App)
