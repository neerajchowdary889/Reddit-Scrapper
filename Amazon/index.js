const puppeteer = require('puppeteer-core');
const fs = require('fs');
const connectionURL = 'wss://browser.zenrows.com?apikey=6e3b7985b41612ed70ab325a6da099e945e9bf16&proxy_country=in';

// async function fetchPageHTML(url) {
//     try {
//         const browser = await puppeteer.connect({ browserWSEndpoint: connectionURL });
//         const page = await browser.newPage();
//         await page.goto(url, { waitUntil: 'load', timeout: 0 });
//         const pageHTML = await page.content();
//         await browser.close();
//         return pageHTML;
//     } catch (error) {
//         console.error("Error fetching page HTML:", error);
//         return null;
//     }
// }

// (async () => {
//     const url = 'https://www.amazon.in/s?k=macbooks&crid=3DZ427SF0MAXC&sprefix=macbook%2Caps%2C281&ref=nb_sb_noss_2';
//     const htmlContent = await fetchPageHTML(url);
//     // console.log(htmlContent);
//     const fs = require('fs');
//     fs.writeFileSync('page.html', htmlContent);
//     console.log("Page HTML saved to file");
// })();


async function fetchProductData(searchUrl) {
    const browser = await puppeteer.connect({ browserWSEndpoint: connectionURL });
    const page = await browser.newPage();
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 60000 });

    // Extract product links from the search results page
    const productLinks = await page.$$eval('a.a-link-normal.s-no-outline', links => links.map(link => link.href));

    const products = [];
    for (const link of productLinks) {
        const productPage = await browser.newPage();
        try {
            await retry(async () => {
                await productPage.goto(link, { waitUntil: 'networkidle2', timeout: 60000 });
            }, 3);

            const product = await productPage.evaluate(() => {
                const getText = (selector) => document.querySelector(selector)?.innerText || 'N/A';

                return {
                    title: getText('#productTitle'),
                    description: getText('#feature-bullets'),
                    price: getText('.a-price .a-offscreen'),
                    comments: getText('#acrCustomerReviewText'),
                    rating: getText('.a-icon-alt'),
                    totalPeopleRated: getText('#acrCustomerReviewText'),
                    numberOfBuyers: getText('#olp_feature_div'),
                };
            });

            products.push(product);
        } catch (error) {
            console.error(`Error fetching product data from ${link}:`, error);
        } finally {
            await productPage.close();
        }

        await delay(2000); // Delay to avoid being blocked
    }

    await browser.close();
    return products;
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

async function retry(fn, retries) {
    for (let i = 0; i < retries; i++) {
        try {
            await fn();
            return;
        } catch (error) {
            if (i === retries - 1) throw error;
            console.warn(`Retrying... (${i + 1}/${retries})`);
            await delay(2000);
        }
    }
}

// Usage example
(async () => {
    const searchUrl = 'https://www.amazon.in/s?k=macbooks&crid=3DZ427SF0MAXC&sprefix=macbook%2Caps%2C281&ref=nb_sb_noss_2';

    try {
        const productData = await fetchProductData(searchUrl);
        fs.writeFileSync('data.json', JSON.stringify(productData, null, 2), 'utf-8');
        console.log("Product data saved to data.json");
    } catch (error) {
        console.error("Error fetching product data:", error);
    }
})();