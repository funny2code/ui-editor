import {useEffect} from "react";

import grapesjs from "grapesjs";
import 'grapesjs/dist/css/grapes.min.css'
import websitePlugin from 'grapesjs-preset-webpage';
import basicBlockPlugin from 'grapesjs-blocks-basic'
import formPlugin from 'grapesjs-plugin-forms'

function App() {

  useEffect(() => {
     grapesjs.init({
       container: '#gjs',
       width: '100%',
       plugins: [websitePlugin,basicBlockPlugin,formPlugin],
     })
  },[])

  return (
      <div id="gjs"></div>
  );
}

export default App;
