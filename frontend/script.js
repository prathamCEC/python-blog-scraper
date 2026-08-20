const postsContainer = document.getElementById("posts-container");
const postCount = document.getElementById("post-count");
const loadingMessage = document.getElementById("loading-message");
const errorMessage = document.getElementById("error-message");


async function loadPosts() {

    try {

        const response = await fetch("http://localhost:5000/api/posts");

        if (!response.ok) {
            throw new Error("Failed to fetch posts");
        }

        const posts = await response.json();

        displayPosts(posts);

    } catch (error) {

        console.error("Error loading posts:", error);

        loadingMessage.hidden = true;
        errorMessage.hidden = false;

    }
}


function displayPosts(posts) {

    loadingMessage.hidden = true;

    postCount.textContent = `${posts.length} posts`;

    if (posts.length === 0) {

        postsContainer.innerHTML = `
            <p>No blog posts available.</p>
        `;

        return;
    }

    postsContainer.innerHTML = posts.map(post => {

        const publishedDate = new Date(
            post.published_date
        ).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric"
        });

        return `
            <article class="post-card">

                <h3>${escapeHtml(post.title)}</h3>

                <p class="post-author">
                    By ${escapeHtml(post.author)}
                </p>

                <p class="post-date">
                    ${publishedDate}
                </p>

                <p class="post-summary">
                    ${escapeHtml(post.summary)}
                </p>

                <a class="read-more" href="post.html?id=${post.id}">Read Article →</a>
            </article>
        `;

    }).join("");
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


loadPosts();
