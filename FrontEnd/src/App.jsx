import { Routes, Route } from "react-router-dom";

import Shop from "./pages/shop";
import Contact from "./pages/contactus";
import Home from "./pages/home";
import { CartProvider } from "./components/Cart/cart";
import Login from "./pages/Login/login";
import Purchases from "./pages/purchases";

const App = () => {
  return (
    <CartProvider>
      <Routes>
        <Route path="/home" element={<Home/>} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/purchases" element={<Purchases />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </CartProvider>
  );
}

export default App;