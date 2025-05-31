#!/usr/bin/env python3
"""
Docker MCP Server Runner for Nagatha Assistant

This script provides an interface for the Nagatha Assistant to run and communicate
with the dockerized MCP server via stdio.
"""

import subprocess
import sys
import os
import json
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DockerMCPServer:
    """
    Manages a dockerized MCP server instance for the Nagatha Assistant.
    """
    
    def __init__(self, 
                 container_name: str = "nagatha-mastodon-mcp",
                 image_name: str = "nagatha-mastodon-mcp",
                 env_vars: Optional[Dict[str, str]] = None):
        self.container_name = container_name
        self.image_name = image_name
        self.env_vars = env_vars or {}
        self.process: Optional[subprocess.Popen] = None
    
    def build_image(self, dockerfile_path: str = ".") -> bool:
        """Build the Docker image."""
        try:
            logger.info(f"Building Docker image {self.image_name}...")
            result = subprocess.run([
                "docker", "build", 
                "-t", self.image_name,
                dockerfile_path
            ], check=True, capture_output=True, text=True)
            
            logger.info("Docker image built successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build Docker image: {e}")
            logger.error(f"stdout: {e.stdout}")
            logger.error(f"stderr: {e.stderr}")
            return False
    
    def start_container(self) -> subprocess.Popen:
        """
        Start the MCP server container with stdio communication.
        Returns the subprocess for communication.
        """
        try:
            # Build docker run command
            cmd = [
                "docker", "run",
                "--rm",  # Remove container when it stops
                "--interactive",  # Keep STDIN open
                "--name", self.container_name
            ]
            
            # Add environment variables
            for key, value in self.env_vars.items():
                if value:  # Only add non-empty values
                    cmd.extend(["-e", f"{key}={value}"])
            
            # Add the image name
            cmd.append(self.image_name)
            
            logger.info(f"Starting container: {' '.join(cmd)}")
            
            # Start the container with stdio pipes
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0  # Unbuffered
            )
            
            logger.info(f"Container {self.container_name} started with PID {self.process.pid}")
            return self.process
            
        except Exception as e:
            logger.error(f"Failed to start container: {e}")
            raise
    
    def stop_container(self):
        """Stop the container gracefully."""
        if self.process:
            logger.info("Stopping MCP server container...")
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("Container didn't stop gracefully, forcing...")
                self.process.kill()
            
            self.process = None
        
        # Ensure container is removed
        try:
            subprocess.run([
                "docker", "rm", "-f", self.container_name
            ], capture_output=True, check=False)
        except Exception:
            pass  # Container might not exist
    
    def send_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a JSON-RPC message to the MCP server and get response."""
        if not self.process:
            raise RuntimeError("Container not started")
        
        try:
            # Send the message
            message_json = json.dumps(message) + "\n"
            logger.debug(f"Sending: {message_json.strip()}")
            
            self.process.stdin.write(message_json)
            self.process.stdin.flush()
            
            # Read the response
            response_line = self.process.stdout.readline()
            if not response_line:
                logger.error("No response from MCP server")
                return None
            
            logger.debug(f"Received: {response_line.strip()}")
            return json.loads(response_line)
            
        except Exception as e:
            logger.error(f"Error communicating with MCP server: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check if the container is healthy and responding."""
        if not self.process:
            return False
        
        # Check if process is still running
        if self.process.poll() is not None:
            return False
        
        try:
            # Send a simple initialize request
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "1.0.0",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "nagatha-assistant",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = self.send_message(init_message)
            return response is not None and "result" in response
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


def main():
    """Example usage of the DockerMCPServer."""
    
    # Get environment variables
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "MASTODON_ACCESS_TOKEN": os.getenv("MASTODON_ACCESS_TOKEN"),
        "MASTODON_API_BASE": os.getenv("MASTODON_API_BASE"),
        "USE_LLM_ACTIVITY": os.getenv("USE_LLM_ACTIVITY", "false"),
        "USE_LLM_TRIAGE": os.getenv("USE_LLM_TRIAGE", "false"),
    }
    
    server = DockerMCPServer(env_vars=env_vars)
    
    try:
        # Build the image
        if not server.build_image():
            sys.exit(1)
        
        # Start the container
        process = server.start_container()
        
        # Health check
        if server.health_check():
            logger.info("✅ MCP server is healthy and ready")
        else:
            logger.error("❌ MCP server health check failed")
            sys.exit(1)
        
        # Keep running (in real usage, Nagatha Assistant would manage this)
        logger.info("MCP server is running. Press Ctrl+C to stop.")
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("Stopping MCP server...")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        server.stop_container()


if __name__ == "__main__":
    main() 