import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getBlogPosts } from '../services/blogService';
import { Calendar, Clock, ArrowRight } from 'lucide-react';
import './BlogList.css';

const BlogList = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const data = await getBlogPosts();
        setPosts(data);
      } catch (error) {
        console.error("Failed to fetch blog posts", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  return (
    <div className="page-blog">
      <div className="blog-header">
        <h1 className="page-title">Engineering <span className="highlight">Logs</span></h1>
        <p className="page-subtitle">Thoughts on DevOps, System Design, and Life.</p>
      </div>

      {loading ? (
        <div className="loading-state">Fetching Articles...</div>
      ) : (
        <div className="blog-grid">
          {posts.map((post) => (
            <Link to={`/blog/${post.slug}`} key={post.id} className="blog-card animate-fade-in">
              {/* Cover Image */}
              <div className="blog-image-wrapper">
                 {post.cover_image_url ? (
                    <img src={post.cover_image_url} alt={post.title} />
                 ) : (
                    <div className="blog-placeholder-img"></div>
                 )}
              </div>

              <div className="blog-content">
                <div className="blog-meta">
                  <span><Calendar size={14} /> {new Date(post.created_at).toLocaleDateString()}</span>
                  <span><Clock size={14} /> {post.read_time} min read</span>
                </div>
                
                <h2 className="blog-title">{post.title}</h2>
                <p className="blog-excerpt">
                  {post.content.substring(0, 100)}...
                </p>

                <div className="read-more">
                   Read Article <ArrowRight size={16} />
                </div>
              </div>
            </Link>
          ))}
          
          {posts.length === 0 && (
            <div className="empty-state">No articles published yet.</div>
          )}
        </div>
      )}
    </div>
  );
};

export default BlogList;