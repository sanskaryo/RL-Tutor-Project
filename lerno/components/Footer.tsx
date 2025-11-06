











// components/Footer.tsx
"use client";

import React from "react";
import { FaGithub, FaXTwitter, FaLinkedin, FaInstagram, FaHeart, FaRobot } from "react-icons/fa6";
import { motion } from "framer-motion";

const Footer: React.FC = () => (
  <footer className="bg-black border-t border-[#232323] pt-12 pb-6 px-4 mt-20">
    <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:justify-between gap-12">
      <div className="flex-1 min-w-[200px]">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center mb-4"
        >
          <span className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-md w-10 h-10 flex items-center justify-center mr-3">
            <span className="text-white font-bold text-xl">L</span>
          </span>
          <span className="text-white font-bold text-lg tracking-wide">
            Lerno AI
          </span>
        </motion.div>
        <p className="text-gray-400 text-sm mb-4">
          Your AI companion for smarter, adaptive, and interactive learning.
        </p>
        <div className="flex space-x-4 mt-2">
          <a
            href="https://github.com/sanskaryo"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub"
            className="transform hover:scale-110 transition-transform"
          >
            <FaGithub
              className="text-gray-400 hover:text-white transition"
              size={22}
            />
          </a>
          <a
            href="https://x.com/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="X (Twitter)"
            className="transform hover:scale-110 transition-transform"
          >
            <FaXTwitter
              className="text-gray-400 hover:text-white transition"
              size={22}
            />
          </a>
          <a
            href="https://linkedin.com/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn"
            className="transform hover:scale-110 transition-transform"
          >
            <FaLinkedin
              className="text-gray-400 hover:text-white transition"
              size={22}
            />
          </a>
          <a
            href="https://instagram.com/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Instagram"
            className="transform hover:scale-110 transition-transform"
          >
            <FaInstagram
              className="text-gray-400 hover:text-white transition"
              size={22}
            />
          </a>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-2 md:grid-cols-3 gap-8 text-sm">
        <div>
          <h4 className="text-white font-semibold mb-3">Resources</h4>
          <ul className="space-y-2">
            <li>
              <a
                href="/about"
                className="text-gray-400 hover:text-white transition"
              >
                About
              </a>
            </li>
            <li>
              <a
                href="/features"
                className="text-gray-400 hover:text-white transition"
              >
                Features
              </a>
            </li>
            <li>
              <a
                href="/pricing"
                className="text-gray-400 hover:text-white transition"
              >
                Pricing
              </a>
            </li>
            <li>
              <a
                href="/faq"
                className="text-gray-400 hover:text-white transition"
              >
                FAQ
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Community</h4>
          <ul className="space-y-2">
            <li>
              <a
                href="/blog"
                className="text-gray-400 hover:text-white transition"
              >
                Blog
              </a>
            </li>
            <li>
              <a
                href="/forum"
                className="text-gray-400 hover:text-white transition"
              >
                Forum
              </a>
            </li>
            <li>
              <a
                href="/events"
                className="text-gray-400 hover:text-white transition"
              >
                Events
              </a>
            </li>
            <li>
              <a
                href="/discord"
                className="text-gray-400 hover:text-white transition"
              >
                Discord
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Contact</h4>
          <ul className="space-y-2">
            <li>
              <a
                href="mailto:support@lerno.ai"
                className="text-gray-400 hover:text-white transition"
              >
                support@lerno.ai
              </a>
            </li>
            <li>
              <a
                href="/contact"
                className="text-gray-400 hover:text-white transition"
              >
                Contact Form
              </a>
            </li>
            <li>
              <a
                href="/privacy"
                className="text-gray-400 hover:text-white transition"
              >
                Privacy Policy
              </a>
            </li>
            <li>
              <a
                href="/terms"
                className="text-gray-400 hover:text-white transition"
              >
                Terms of Service
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div className="border-t border-[#232323] mt-10 pt-6 flex flex-col items-center space-y-4">
      <div className="flex items-center text-gray-400 text-sm">
        <span>Made with</span>
        <FaHeart className="text-red-500 mx-1 animate-pulse" />
        <span>by Team T50:</span>
        <motion.span 
          className="ml-2 font-medium bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent"
          whileHover={{ scale: 1.05 }}
        >
          Sanskar, Ayush, Krishna
        </motion.span>
      </div>
      
      <div className="flex items-center text-gray-400 text-sm">
        <span>Powered by</span>
        <FaRobot className="text-blue-500 mx-1" />
        <motion.span 
          className="font-medium bg-gradient-to-r from-blue-400 to-cyan-600 bg-clip-text text-transparent"
          whileHover={{ scale: 1.05 }}
        >
          Reinforcement Learning
        </motion.span>
        <span className="mx-1">&</span>
        <motion.span 
          className="font-medium bg-gradient-to-r from-green-400 to-emerald-600 bg-clip-text text-transparent"
          whileHover={{ scale: 1.05 }}
        >
          Generative AI
        </motion.span>
      </div>

      <div className="text-gray-500 text-xs">
        &copy; {new Date().getFullYear()} Lerno AI. All rights reserved.
      </div>
    </div>
  </footer>
);

export default Footer;