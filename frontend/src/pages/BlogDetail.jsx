import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { getBlogPostBySlug } from '../services/blogService';
import { ArrowLeft, Calendar, Clock, Tag } from 'lucide-react';
import './BlogDetail.css';

const BlogDetail = () => {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const data = await getBlogPostBySlug(slug);
        setPost(data);
      } catch (error) {
        console.error("Failed to load post", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPost();
  }, [slug]);

  if (loading) return <div className="loading-state">Loading Post...</div>;
  if (!post) return <div className="loading-state">Post not found.</div>;

  return (
    <div className="page-blog-detail">
      <Link to="/blog" className="back-link">
        <ArrowLeft size={16} /> Back to Logs
      </Link>

      <article className="blog-article animate-fade-in">
        <header className="article-header">
          <div className="article-meta">
            <span><Calendar size={14} /> {new Date(post.created_at).toLocaleDateString()}</span>
            <span><Clock size={14} /> {post.read_time} min read</span>
          </div>
          <h1 className="article-title">{post.title}</h1>
          <div className="article-tags">
            {post.tags.split(',').map((tag, i) => (
                <span key={i} className="tag-pill"><Tag size={12}/> {tag.trim()}</span>
            ))}
          </div>
        </header>
        
        {post.cover_image_url && (
        <div className="article-cover">
          <img src={post.cover_image_url} alt={post.title} />
        </div>
      )}

        <div className="article-content">
          <ReactMarkdown>{post.content}</ReactMarkdown>
        </div>
      </article>
    </div>
  );
};

export default BlogDetail;