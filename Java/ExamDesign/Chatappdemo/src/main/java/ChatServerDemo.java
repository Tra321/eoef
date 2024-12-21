import java.io.*;
import java.net.*;
import java.util.*;
import java.util.logging.*;

public class ChatServerDemo {
    private static final Logger logger = Logger.getLogger(ChatServerDemo.class.getName());
    private static final Map<String, Socket> clientMap = Collections.synchronizedMap(new HashMap<>());

    static {
        ConsoleHandler handler = new ConsoleHandler();
        handler.setFormatter(new SimpleFormatter() {
            @Override
            public String format(LogRecord record) {
                return String.format("[%s] %s: %s%n",
                        record.getLevel(),
                        record.getSourceClassName(),
                        record.getMessage());
            }
        });
        logger.addHandler(handler);
        logger.setLevel(Level.ALL);
    }

    public static void main(String[] args) throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            logger.info("服务器启动成功，正在监听端口 12345...");
            logger.info("本机地址: " + InetAddress.getLocalHost().getHostAddress());

            while (!Thread.currentThread().isInterrupted()) {
                try {
                    logger.info("等待客户端连接...");
                    Socket clientSocket = serverSocket.accept();
                    logger.info("新客户端连接成功！客户端地址: " +
                            clientSocket.getInetAddress().getHostAddress());
                    new Thread(new ClientHandler(clientSocket)).start();
                } catch (IOException e) {
                    logger.log(Level.WARNING, "接受客户端连接时发生错误", e);
                    if (serverSocket.isClosed()) {
                        break;
                    }
                }
            }
        } catch (IOException e) {
            logger.log(Level.SEVERE, "服务器启动失败", e);
            throw e;
        }
    }

    static class ClientHandler implements Runnable {
        private final Socket socket;
        private final String username;
        private final BufferedReader in;
        private final PrintWriter out;

        public ClientHandler(Socket socket) throws IOException {
            this.socket = socket;
            this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.out = new PrintWriter(socket.getOutputStream(), true);
            try {
                logger.info("等待客户端发送用户名...");
                this.username = in.readLine();
                logger.info("收到用户名: " + username);

                if (this.username == null || this.username.trim().isEmpty()) {
                    logger.warning("用户名无效");
                    throw new IOException("Invalid username");
                }
                if (clientMap.containsKey(this.username)) {
                    logger.warning("用户名已存在: " + this.username);
                    out.println("用户名已存在，请选择其他用户名");
                    throw new IOException("Username already exists");
                }
            } catch (IOException e) {
                closeResources();
                throw e;
            }
        }

        private void closeResources() {
            try {
                if (in != null) in.close();
                if (out != null) out.close();
                if (socket != null) socket.close();
            } catch (IOException e) {
                logger.log(Level.WARNING, "关闭资源时发生错误", e);
            }
        }

        @Override
        public void run() {
            try (socket; in; out) {  // 使用 try-with-resources
                clientMap.put(username, socket);
                logger.info("新用户 " + username + " 成功加入聊天室");
                broadcast(username + " has joined the chat!");

                String message;
                logger.info("开始监听用户 " + username + " 的消息");
                while ((message = in.readLine()) != null) {
                    logger.info("收到来自 " + username + " 的消息: " + message);
                    broadcast(username + ": " + message);
                }
            } catch (IOException e) {
                logger.log(Level.WARNING, "处理客户端 " + username + " 时发生错误", e);
            } finally {
                logger.info("用户 " + username + " 断开连接");
                closeResources();
                clientMap.remove(username);
                broadcast(username + " has left the chat.");
            }
        }

        private void broadcast(String message) {
            Iterator<Map.Entry<String, Socket>> iterator = clientMap.entrySet().iterator();
            while (iterator.hasNext()) {
                Map.Entry<String, Socket> entry = iterator.next();
                Socket client = entry.getValue();
                try {
                    PrintWriter clientOut = new PrintWriter(client.getOutputStream(), true);
                    clientOut.println(message);
                } catch (IOException e) {
                    logger.log(Level.WARNING, "广播消息时发生错误", e);
                    iterator.remove();
                    try {
                        client.close();
                    } catch (IOException ex) {
                        logger.log(Level.WARNING, "关闭失效客户端连接时发生错误", ex);
                    }
                }
            }
        }
    }
}