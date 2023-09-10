import logo from './logo.svg';
import './App.css';
import './style.css'
import './Components/Navbar'
import Navbar from './Components/Navbar';
import Home from './Components/HomePage/Home';
import Mess from './Components/Mess/Mess';
import Outlet from './Components/Outlets/Outlet';
import Bus from './Components/BusSchedule/Bus';
import {Routes,Route} from 'react-router-dom';

function App() {
  return (
    <>
    <Navbar/>
    <Routes>
      <Route path='/' element={<Home/>}></Route>
      <Route path='/mess' element={<Mess/>}></Route>
      <Route path='/bus' element={<Bus/>}></Route>
    </Routes>
    
    </>
  );
}

export default App;
