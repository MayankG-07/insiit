import { Link } from "react-router-dom";
function Navbar() {
    return(
        <>

        <div className="navbar">
            <Link to='/' href="#">Home</Link>
            <Link to="/mess">Mess</Link>
            <Link to="/outlet">Outlets</Link>
            <Link to="/bus">Bus Schedule</Link>
        </div>
        </>
    )
}
export default Navbar;