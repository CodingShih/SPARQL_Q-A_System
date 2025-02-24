// src/components/Posts.js
import React, { useState, useEffect } from 'react';


const Posts = () => {

  const [posts, setPosts] = useState([]);

  // RESTful API
  useEffect(() => 
    {
    fetch('/api/posts')
      .then(response => response.json())
      .then(data => setPosts(data));
    }, []);

    return (
      <div>
        <h1>這裡專門放置部落格的文章</h1>
        {/* 这里可以映射并展示博客文章列表 */}
        <ul>
          {posts.map(post => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      </div>
    );

  
};

export default Posts;
