// Initialize variable for postCardMacro and postContainer
let postCardMacro;
let postContainer;

// Limit
let limit = 6;
// Offset
let offset = 0;

// Id of div elements and hidden input values
let homeSpinner = document.getElementById("homeSpinner");
let loadMoreSpinner = document.getElementById("loadMoreSpinner");
let currentCategory = document.getElementById("currentCategoryText");
let loadMoreButtonDiv = document.getElementById("loadMoreButton");
const sortBy = document.getElementById("currentSortText");
const orderby = document.getElementById("currentOrderText");

// Categories and associated icons
const categoryList = {
    'Games': '<a href="/category/Games"><i class="ti ti-device-gamepad text-rose-500 hover:text-rose-600 duration-150"></i></a>',
    'History': '<a href="/category/History"><i class="ti ti-books text-sky-500 hover:text-sky-600 duration-150"></i></a>',
    'Science': '<a href="/category/Science"><i class="ti ti-square-root-2 text-emerald-500 hover:text-emerald-600 duration-150"></i></a>',
    'Code': '<a href="/category/Code"><i class="ti ti-code text-indigo-500 hover:text-indigo-600 duration-150"></i></a>',
    'Technology': '<a href="/category/Technology"><i class="ti ti-cpu text-slate-500 hover:text-slate-600 duration-150"></i></a>',
    'Education': '<a href="/category/Education"><i class="ti ti-school text-blue-500 hover:text-blue-600 duration-150"></i></a>',
    'Sports': '<a href="/category/Sports"><i class="ti ti-shirt-sport text-cyan-500 hover:text-cyan-600 duration-150"></i></a>',
    'Foods': '<a href="/category/Foods"><i class="ti ti-meat text-lime-500 hover:text-lime-600 duration-150"></i></a>',
    'Health': '<a href="/category/Health"><i class="ti ti-heartbeat text-red-500 hover:text-red-600 duration-150"></i></a>',
    'Apps': '<a href="/category/Apps"><i class="ti ti-apps text-pink-500 hover:text-pink-600 duration-150"></i></a>',
    'Movies': '<a href="/category/Movies"><i class="ti ti-movie text-teal-500 hover:text-teal-600 duration-150"></i></a>',
    'Series': '<a href="/category/Series"><i class="ti ti-player-play text-yellow-500 hover:text-yellow-600 duration-150"></i></a>',
    'Travel': '<a href="/category/Travel"><i class="ti ti-plane text-zinc-500 hover:text-zinc-600 duration-150"></i></a>',
    'Books': '<a href="/category/Books"><i class="ti ti-book text-violet-500 hover:text-violet-600 duration-150"></i></a>',
    'Music': '<a href="/category/Music"><i class="ti ti-music text-orange-500 hover:text-orange-600 duration-150"></i></a>',
    'Nature': '<a href="/category/Nature"><i class="ti ti-trees text-emerald-500 hover:text-emerald-600 duration-150"></i></a>',
    'Art': '<a href="/category/Art"><i class="ti ti-brush text-amber-500 hover:text-amber-600 duration-150"></i></a>',
    'Finance': '<a href="/category/Finance"><i class="ti ti-coin text-green-500 hover:text-green-600 duration-150"></i></a>',
    'Business': '<a href="/category/Business"><i class="ti ti-tie text-stone-500 hover:text-stone-600 duration-150"></i></a>',
    'Web': '<a href="/category/Web"><i class="ti ti-world text-purple-500 hover:text-purple-600 duration-150"></i></a>',
    'Other': '<a href="/category/Other"><i class="ti ti-dots text-gray-500 hover:text-gray-600 duration-150"></i></a>',
    'Default': '<a href="/"><i class="ti ti-stack-2 text-neutral-500 hover:text-neutral-600 duration-150"></i></a>'
};

// Function to inject html post macro in document body
async function intializePostCard() {
    fetch(postCardMacroPath)
        .then(res => res.text())
        .then(postCardHtml => {
            // Insert the fetched template into a hidden container
            const tempContainer = document.createElement('div');
            tempContainer.innerHTML = postCardHtml;

            // Register macro in dome
            document.body.appendChild(tempContainer); // or keep it detached

            /// Assign html element's id of content to variable
            postCardMacro = document.getElementById("postCardMacro");
            postContainer = document.getElementById("postCardContainer");
        });
}
// Call initialize post card function to inject post macro
intializePostCard();

// Function to fetch homeFeedData from backend
async function fetchHomeFeedData() {
    try {
        let connection = await fetch(`/api/v1/homeFeedData?category=${currentCategory.value}&by=${sortBy.value}&sort=${orderby.value}&limit=${limit}&offset=${offset}`);
        let res = await connection.json();

        if (connection.ok) {
            let posts = res.payload;

            posts.forEach(post => {
                const clone = postCardMacro.content.cloneNode(true);
                clone.querySelector(".postTitle").innerText = post.title;
                clone.querySelector(".postTitle").href = post.postLink;
                clone.querySelector(".postContent").innerHTML = post.content;
                clone.querySelector(".postBanner").src = post.bannerImgSrc;
                clone.querySelector(".postAuthorPicture").src = post.authorProfile;
                clone.querySelector(".postAuthor").innerText = post.author;
                clone.querySelector(".postAuthor").href = `/user/${post.author}`;
                clone.querySelector(".postCategory").innerHTML = categoryList[post.category] || categoryList["Default"];
                clone.querySelector(".postTimeStamp").innerText = post.timeStamp;
                postContainer.appendChild(clone);
            });

            // Increase the offset with the value of limit
            offset += limit;
            
            // Check if posts length is not less than limit
            if (posts.length < limit) {
                // Hide button
                loadMoreButtonDiv.classList.add("hidden");
            }
        } else {
            // Print error on console
            console.error(connection.status);
        }
    } catch (error) {
        // Print error on console
        console.error(error);
    }
}

async function loadMoreButton() {
    // Show spinner
    loadMoreSpinner.classList.remove("hidden");
    // Fetch homeFeed
    await fetchHomeFeedData();
    // Hide spinner
    loadMoreSpinner.classList.add("hidden");
}

// Call the function to load data
window.onload = async function () {
    // Show spinner
    homeSpinner.classList.remove("hidden");
    // Fetch initial homeFeed
    await fetchHomeFeedData();
    // Hide spinner
    homeSpinner.classList.add("hidden");
}