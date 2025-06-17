import React, { useState } from 'react';
// import Navbar from './components/Navbar/navbar';
import { Route, Routes } from 'react-router-dom';
import Cart from './pages/cart/cart';
import PlaceOrder from './pages/placeOrder/placeOrder';
import Footer from './components/footer/footer';
import LoginPopup from './components/loginPopup/loginPopup';
import { AdminRoutes } from './classWork/Foods/admin/AdminRoutes';
// import Home from './pages/home/home';
import './css/index.css';



// import Home from './classWork/Foods/Home';
// import AddFood from './classWork/Foods/addFood';
// import DeleteFood from './classWork/Foods/deleteFood';
// import UpdataFood from './classWork/Foods/updataFood';
// import AddMenu from './classWork/Foods/AddMenu';
// import DeleteMenu from './classWork/Foods/DeleteMenu';
// import UpdataMenu from './classWork/Foods/UpdataMenu';
// import Nav from './classWork/Foods/nav/navbar';
// import Footr from './classWork/Foods/Footer';
// import CartPay from './classWork/Foods/Cart';
// import { ToastContainer } from "react-toastify";
// import OrdersManager from './classWork/Foods/OrderManger';
// import CommentPage from './classWork/Foods/CommentPage';


import Home from './instagram/home/Home';
import Login from './instagram/components/login/Login';
import Profile from './instagram/profile/Profile';
import { ToastContainer } from 'react-toastify';
import EditProfile from './instagram/profile/EditProfile';
import UserProfile from './instagram/profile/UserProfile/UserProfile';
import FollowingPosts from './instagram/timeline/homePosts/FollowingPosts';


function App(){

    const [showlogin, setShowLogin] = useState(false);

    return(

        <div>
            <ToastContainer/>
            <Routes>
                <Route path='/login' element={<Login/>}/>
                <Route path='/' element={<Home/>}>
                    <Route path='/profile' element={<Profile/>}/> 
                    <Route path='/user-profile/:id' element={<UserProfile/>}/>   
                    <Route path='/' element={<FollowingPosts/>}/>  
                    <Route path='/edit' element={<EditProfile/>}/>        
                </Route>
            </Routes>
        </div>



        // <div >
        //     <ToastContainer/>
        //     <Routes>
        //         <Route path='/*' element={
        //             <div>
        //                 <div className='app'>
        //                 <Nav/>
        //                 <Routes>
        //                     <Route path="/" element={<Home/>}/>
        //                     <Route path="/add-food" element={<AddFood/>}/>
        //                     <Route path="/food-list" element={<DeleteFood/>}/>
        //                     <Route path="/update-food/:id" element={<UpdataFood/>}/>
        //                     <Route path="/add-menu" element={<AddMenu/>}/>
        //                     <Route path="/menu-list" element={<DeleteMenu/>}/>
        //                     <Route path="/updata-menu/:id" element={<UpdataMenu/>}/>
        //                     <Route path="/cart" element={<CartPay/>}/>
        //                     <Route path="/orders-manager" element={<OrdersManager/>}/> 
        //                     <Route path="/comments/:id" element={<CommentPage />} />
        //                 </Routes>
        //             </div>
        //             <Footr/>
        //             </div> 
        //         }/>
        //         <Route path="/admin-panel/*"element={<AdminRoutes/>}/>
        //     </Routes>
        // </div>
        









        // <div>
        //     {showlogin ? <LoginPopup setShowLogin={setShowLogin}/> : <></>}
        
        //         <Routes>
        //             <Route path="/*" element={
        //                 <div>
        //                     <div className='app'>
        //                         <Navbar setShowLogin={setShowLogin} />
        //                         <Routes>
        //                             <Route path="/" element={<Home />} />
        //                             <Route path="/cart" element={<Cart />} />
        //                             <Route path="/order" element={<PlaceOrder />} />
        //                         </Routes>
        //                     </div>
        //                     <Footer/>
        //                 </div>
        //             } /> 
        //             <Route path="/admin-panel/*"element={<AdminRoutes/>}/>    
        //         </Routes>
        // </div>

        
        
    )   
}
export default App;