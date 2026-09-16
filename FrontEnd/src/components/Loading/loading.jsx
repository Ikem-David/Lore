import './loading.css';

const Loading = () => {
    return (
        <main className="LoadingPage" role="status" aria-live="polite" aria-label="Loading the collection">
            <div className="LoadingBrand" aria-hidden="true">
                <span>LORE</span>
            </div>
            <div className="LoadingContent">
                <p className="LoadingEyebrow">THE COLLECTION</p>
                <h1>Curating your edit</h1>
                <div className="LoadingTrack" aria-hidden="true">
                    <span />
                </div>
                <p className="LoadingMessage">A moment while we bring everything into view.</p>
            </div>
            <p className="LoadingIndex" aria-hidden="true">01 / 03</p>
        </main>
    );
};

export default Loading;
