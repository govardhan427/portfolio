import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { trackVisitor } from '../../../services/portfolioService';

const useVisitorTracker = () => {
    const location = useLocation();

    useEffect(() => {
        // Whenever the route (location.pathname) changes, run this:
        trackVisitor(location.pathname);
    }, [location]);
};

export default useVisitorTracker;