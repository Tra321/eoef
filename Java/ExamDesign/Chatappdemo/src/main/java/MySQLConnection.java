import java.sql.*;
import java.util.logging.*;

public class MySQLConnection {
    private static final Logger logger = Logger.getLogger(MySQLConnection.class.getName());
    private static final String URL = "jdbc:mysql://localhost:3306/chatapp?characterEncoding=utf-8";
    private static final String USER = "root";
    private static final String PASSWORD = "Mysql135!";

    static {
        try {
            // 加载MySQL驱动
            Class.forName("com.mysql.cj.jdbc.Driver");
            logger.info("MySQL驱动加载成功");
        } catch (ClassNotFoundException e) {
            logger.log(Level.SEVERE, "MySQL驱动加载失败: " + e.getMessage(), e);
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }

    public static boolean validateUser(String username, String password) {
        String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, username);
            pstmt.setString(2, password);

            try (ResultSet rs = pstmt.executeQuery()) {
                return rs.next();
            }
        } catch (SQLException e) {
            logger.severe("验证用户失败: " + e.getMessage());
            return false;
        }
    }

    public static boolean registerUser(String username, String password) {
        String sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, username);
            pstmt.setString(2, password);

            return pstmt.executeUpdate() > 0;
        } catch (SQLException e) {
            logger.severe("注册用户失败: " + e.getMessage());
            return false;
        }
    }
}