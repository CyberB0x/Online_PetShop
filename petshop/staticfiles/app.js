document.addEventListener("DOMContentLoaded", async () => {
    const productsDiv = document.getElementById("products");

    try {
        const response = await fetch("/api/products/");
        const products = await response.json();

        products.forEach(p => {
            const card = document.createElement("div");
            card.className = "product";
            card.innerHTML = `
                <h3>${p.name}</h3>
                <p>Price: ${p.price}₺</p>
            `;
            productsDiv.appendChild(card);
        });
    } catch (err) {
        productsDiv.innerHTML = "<p>⚠️ Failed to load products</p>";
    }
});
