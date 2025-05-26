const { useState, useEffect } = React;

function ListingForm({ listing, onSuccess }) {
  const [formData, setFormData] = useState(listing || {});

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const method = listing ? 'PUT' : 'POST';
    const url = listing ? `/api/listings/${listing.id}/` : '/api/listings/';
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then(res => res.json())
      .then(() => onSuccess())
      .catch(err => console.error(err));
  };

  return (
    <form onSubmit={handleSubmit} className="mb-3">
      <div className="row g-2">
        <div className="col-md-6">
          <input className="form-control" placeholder="Street" name="street" value={formData.street || ''} onChange={handleChange} />
        </div>
        <div className="col-md-6">
          <input className="form-control" placeholder="City" name="city" value={formData.city || ''} onChange={handleChange} />
        </div>
      </div>
      <div className="row g-2 mt-2">
        <div className="col-md-4">
          <input className="form-control" placeholder="State" name="state" value={formData.state || ''} onChange={handleChange} />
        </div>
        <div className="col-md-4">
          <input className="form-control" placeholder="Zip" name="zip" value={formData.zip || ''} onChange={handleChange} />
        </div>
        <div className="col-md-4">
          <input className="form-control" placeholder="Bedrooms" name="bedrooms" type="number" value={formData.bedrooms || ''} onChange={handleChange} />
        </div>
      </div>
      <div className="row g-2 mt-2">
        <div className="col-md-4">
          <input className="form-control" placeholder="Bathrooms" name="bathrooms" type="number" value={formData.bathrooms || ''} onChange={handleChange} />
        </div>
        <div className="col-md-4">
          <select className="form-select" name="property_type" value={formData.property_type || ''} onChange={handleChange}>
            <option value="">Type</option>
            <option value="house">House</option>
            <option value="apartment">Apartment</option>
            <option value="condo">Condo</option>
            <option value="group_home">Group Home</option>
          </select>
        </div>
        <div className="col-md-4 form-check form-switch text-start mt-2">
          <input className="form-check-input" type="checkbox" name="is_available" checked={formData.is_available || false} onChange={handleChange} />
          <label className="form-check-label ms-2">Available</label>
        </div>
      </div>
      <button className="btn btn-primary mt-3" type="submit">Save</button>
    </form>
  );
}

function App() {
  const [listings, setListings] = useState([]);
  const [view, setView] = useState('list');
  const [current, setCurrent] = useState(null);

  const loadListings = () => {
    fetch('/api/listings/')
      .then(res => res.json())
      .then(data => setListings(data));
  };

  useEffect(() => {
    loadListings();
  }, []);

  const showDetail = (id) => {
    fetch(`/api/listings/${id}/`)
      .then(res => res.json())
      .then(data => { setCurrent(data); setView('detail'); });
  };

  const deleteListing = (id) => {
    fetch(`/api/listings/${id}/`, { method: 'DELETE' })
      .then(() => loadListings());
  };

  if (view === 'form') {
    return (
      <div className="container mt-4">
        <button className="btn btn-secondary mb-3" onClick={() => { setView('list'); setCurrent(null); }}>Back</button>
        <ListingForm listing={current} onSuccess={() => { setView('list'); loadListings(); }} />
      </div>
    );
  }

  if (view === 'detail' && current) {
    return (
      <div className="container mt-4">
        <button className="btn btn-secondary mb-3" onClick={() => setView('list')}>Back</button>
        <h3>{current.street}</h3>
        <p>{current.city}, {current.state} {current.zip}</p>
        <p>Bedrooms: {current.bedrooms}</p>
        <p>Bathrooms: {current.bathrooms}</p>
        <button className="btn btn-primary me-2" onClick={() => { setView('form'); }}>Edit</button>
        <button className="btn btn-danger" onClick={() => { deleteListing(current.id); setView('list'); }}>Delete</button>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between mb-3">
        <h2>Listings</h2>
        <button className="btn btn-success" onClick={() => setView('form')}>Add</button>
      </div>
      <table className="table table-dark table-bordered">
        <thead>
          <tr>
            <th>Street</th>
            <th>City</th>
            <th>State</th>
            <th>Zip</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {listings.map(l => (
            <tr key={l.id}>
              <td>{l.street}</td>
              <td>{l.city}</td>
              <td>{l.state}</td>
              <td>{l.zip}</td>
              <td>
                <button className="btn btn-info btn-sm me-2" onClick={() => showDetail(l.id)}>View</button>
                <button className="btn btn-warning btn-sm me-2" onClick={() => { setCurrent(l); setView('form'); }}>Edit</button>
                <button className="btn btn-danger btn-sm" onClick={() => deleteListing(l.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
