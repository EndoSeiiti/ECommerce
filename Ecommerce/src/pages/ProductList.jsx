import { useState, useEffect } from 'react'

function ProductList() {
  const[products, setProducts] = useState([])
  const[error, setError] = useState(null) 

  useEffect(()=>{
   const fetchProducts = async() => {
    try{
      const response =await fetch ('http://localhost:5000/api/products')
      if (!response.ok){
        throw new Error("Error, couldn't retrieve products")
      }
      const data = await response.json();
      setProducts(data);
    }
    catch (err){(err.message);}
    };

    fetchProducts();
  },[]);

  if (error){return <div>Error</div>;}
  return (
   <div className='container'>
    <h1>Catalogue</h1>
    <div className='products grid'>
      {products.map(product =>(
      <div key={product.id} className='product-card'>
        <img src={product.image_url} alt={product.name} />
        <h2>{product.name}</h2>
        <p>$ {product.price.toFixed(2)}</p>
      </div>
      ))}

    </div>

   </div>
  );
}

export default ProductList
