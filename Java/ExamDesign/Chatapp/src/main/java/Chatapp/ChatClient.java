package Chatapp;
import java.io.*;
import java.net.*;
import javax.swing.*;
import java.awt.*;
import java.util.logging.*;

public class ChatClient {
    private static final Logger logger = Logger.getLogger(ChatClient.class.getName());

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

    public static void main(String[] args) {
        try {
            String serverIP = JOptionPane.showInputDialog(
                    null,
                    "请输入服务器IP地址:",
                    "服务器连接",
                    JOptionPane.QUESTION_MESSAGE
            );

            if (serverIP == null || serverIP.trim().isEmpty()) {
                serverIP = "localhost";
            }

            System.out.println("正在尝试连接服务器: " + serverIP + "...");
            Socket socket = new Socket(serverIP, 12345);
            System.out.println("成功连接到服务器！");
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            String username = JOptionPane.showInputDialog(
                    null,
                    "请输入用户名:",
                    "用户名",
                    JOptionPane.QUESTION_MESSAGE
            );

            if (username == null || username.trim().isEmpty()) {
                JOptionPane.showMessageDialog(null, "用户名不能为空！");
                socket.close();
                return;
            }

            out.println(username);

            JFrame frame = new JFrame("聊天客户端 - " + username);
            JTextArea chatArea = new JTextArea(20, 40);
            chatArea.setEditable(false);
            JTextField inputField = new JTextField(35);
            JButton sendButton = new JButton("发送");

            JPanel inputPanel = new JPanel();
            inputPanel.add(inputField);
            inputPanel.add(sendButton);

            frame.setLayout(new BorderLayout());
            frame.add(new JScrollPane(chatArea), BorderLayout.CENTER);
            frame.add(inputPanel, BorderLayout.SOUTH);

            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);

            inputField.requestFocusInWindow();

            inputField.addActionListener(e -> {
                String message = inputField.getText();
                if (!message.trim().isEmpty()) {
                    try {
                        out.println(message);
                        System.out.println("发送消息: " + message);
                        inputField.setText("");
                        inputField.requestFocusInWindow();
                    } catch (Exception ex) {
                        logger.log(Level.SEVERE, "发送消息失败", ex);
                        JOptionPane.showMessageDialog(frame, "发送消息失败: " + ex.getMessage());
                    }
                }
            });

            sendButton.addActionListener(e -> {
                String message = inputField.getText();
                if (!message.trim().isEmpty()) {
                    try {
                        out.println(message);
                        System.out.println("发送消息: " + message);
                        inputField.setText("");
                        inputField.requestFocusInWindow();
                    } catch (Exception ex) {
                        logger.log(Level.SEVERE, "发送消息失败", ex);
                        JOptionPane.showMessageDialog(frame, "发送消息失败: " + ex.getMessage());
                    }
                }
            });

            frame.addWindowListener(new java.awt.event.WindowAdapter() {
                @Override
                public void windowClosing(java.awt.event.WindowEvent windowEvent) {
                    try {
                        System.out.println("关闭连接...");
                        socket.close();
                    } catch (IOException e) {
                        logger.log(Level.SEVERE, "关闭连接时发生错误", e);
                    }
                }
            });

            new Thread(() -> {
                try {
                    String message;
                    while (!socket.isClosed() && (message = in.readLine()) != null) {
                        final String finalMessage = message;
                        SwingUtilities.invokeLater(() ->
                                chatArea.append(finalMessage + "\n")
                        );
                    }
                    System.out.println("服务器消息接收结束");
                } catch (IOException e) {
                    if (!socket.isClosed()) {
                        logger.log(Level.SEVERE, "接收消息时发生错误", e);
                        SwingUtilities.invokeLater(() ->
                                JOptionPane.showMessageDialog(frame, "连接已断开: " + e.getMessage())
                        );
                    }
                }
            }).start();

        } catch (ConnectException e) {
            logger.log(Level.SEVERE, "连接服务器失败", e);
            JOptionPane.showMessageDialog(null, "无法连接到服务器，请确保服务器已启动\n错误信息: " + e.getMessage());
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "发生IO异常", ex);
            JOptionPane.showMessageDialog(null, "连接出错: " + ex.getMessage());
        }
    }
}