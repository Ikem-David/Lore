import Navbar from '../components/Navbar/navbar'
import Footer from '../components/Footer/footer'
import { useCart } from '../components/Cart/cart'
import { useEffect, useState } from 'react'; 
import { useSearchParams } from 'react-router-dom';
import useFetch from '../components/useFetch';
import Loading from '../components/Loading/loading';

const Shop = () => {
    const {data,loading,error} = useFetch(
        `${import.meta.env.VITE_API_URL}/product/`
    );
    const [searchParams, setSearchParams] = useSearchParams();
    const requestedCategory = searchParams.get('category');
    const validCategories = ['All', 'Blazers', 'Shirts', 'Gowns'];
    const initialCategory = validCategories.includes(requestedCategory) ? requestedCategory : 'All';
    const [activeTab, setActiveTab] = useState(initialCategory);
    const [message, setMessage] = useState(false);
    const { addItem } = useCart();

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    if (loading) {
        return <Loading />
    }

    if (error) {
        return <p>{error}</p>
    }


    const filteredProducts = activeTab === 'All'
        ? data
        : data.filter((product) => product.categorie === activeTab);

  return (
    <>
        <Navbar/>
        <div className='ShopContainer'>
        {/* Header Section */}
        <div className='ShopHeader'>
            <h1>SHOP THE COLLECTION</h1>
            <p>Everyday fashion, elevated.</p>
        </div>

        {/* Filter Tabs */}
        <div className='ShopTab'>
            {['All', 'Blazers', 'Shirts', 'Gowns'].map((tab) => (
            <button
                key={tab}
                onClick={() => {
                    setActiveTab(tab);
                    setSearchParams(tab === 'All' ? {} : { category: tab });
                }}
                style={{
                background: 'none',
                border: 'none',
                borderBottom: activeTab === tab ? '2px solid #000000' : '2px solid transparent',
                color: activeTab === tab ? '#000000' : '#777777',
                fontWeight: activeTab === tab ? '600' : '400',
                paddingBottom: '4px',
                cursor: 'pointer',
                }}
            >
                {tab}
            </button>
            ))}
        </div>


        {/* Product Grid */}
        <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
            gap: '32px',
        }}>
            {filteredProducts.map((product) => (
            <div key={product.id}>
                <div className='ShopCards' style={{
                    backgroundColor: '#f4f4f4',
                    borderRadius: '20px',
                    aspectRatio: '3/4',
                    position: 'relative',
                    overflow: 'hidden',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '16px',
                }}>
                <img
                    src={product.image_url}
                    alt={product.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '12px' }}
                />
                </div>
                <div style={{
                    marginTop: '16px',
                    display: 'flex',
                    flexDirection:'column',
                    height:'150px',
                    justifyContent: 'space-evenly',
                    alignItems: 'baseline',
                    padding: '0 4px',
                }}>
                    <button
                        className="ShopAddButton"
                        type="button"
                        onClick={() => {
                            addItem(product);
                            setMessage(true)
                            setTimeout(() => setMessage(false), 3000)
                        }}
                    >
                        Add to cart
                    </button>
                <h3 style={{
                    fontFamily: 'serif',
                    fontSize: '18px',
                    color: '#111111',
                    margin: 0,
                }}>{product.name}</h3>
                <span style={{                
                    fontSize: '14px',
                    fontWeight: '600',
                    color: '#333333',
                }}>${product.price}</span>
                </div>
                <p style={{ fontSize: '12px', color: '#888888', margin: '4px 0 0 4px' }}>{product.categorie}</p>
            </div>
            ))}
        </div>
        </div>
        {message && (
            <div className="CartMessage">
                <p role="status">
                    Item Added to Cart
                </p>
            </div>
        )}        
        <Footer/>
    </>
  );
}
export default Shop;