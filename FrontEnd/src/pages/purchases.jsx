import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar/navbar';
import Footer from '../components/Footer/footer';
import Loading from '../components/Loading/loading';
import './purchases.css';

const Purchases = () => {
    const navigate = useNavigate();
    const [purchases, setPurchases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');

        if (!token) {
            navigate('/', { replace: true });
            return;
        }

        const loadPurchases = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/purchases/me`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || 'Unable to load your purchases.');
                }

                setPurchases(data);
            } catch (requestError) {
                if (requestError.message === 'Could not validate credentials') {
                    localStorage.removeItem('token');
                    navigate('/', { replace: true });
                    return;
                }
                setError(requestError.message || 'Unable to load your purchases.');
            } finally {
                setLoading(false);
            }
        };

        loadPurchases();
    }, [navigate]);

    return (
        <div className="purchases-page">
            <Navbar />
            <main className="purchases-main">
                <div className="purchases-heading">
                    <p className="purchases-eyebrow">Your account</p>
                    <h1>Purchase history</h1>
                    <p>Review the orders you have placed with Lore.</p>
                </div>

                {loading && <Loading />}
                {!loading && error && <p className="purchases-error" role="alert">{error}</p>}
                {!loading && !error && purchases.length === 0 && (
                    <div className="purchases-empty">
                        <h2>No purchases yet</h2>
                        <p>Your completed orders will appear here.</p>
                    </div>
                )}
                {!loading && !error && purchases.length > 0 && (
                    <div className="purchases-table-wrap">
                        <table className="purchases-table">
                            <caption className="sr-only">Your purchase history</caption>
                            <thead>
                                <tr>
                                    <th scope="col">Order</th>
                                    <th scope="col">Date</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {purchases.map((purchase) => (
                                    <tr key={purchase.id}>
                                        <th scope="row">#{purchase.id}</th>
                                        <td>{new Date(purchase.created_at).toLocaleDateString()}</td>
                                        <td><span className="purchase-status">Completed</span></td>
                                        <td className="purchase-total">${Number(purchase.total_price).toFixed(2)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>
            <Footer />
        </div>
    );
};

export default Purchases;
