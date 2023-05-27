import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


# Definindo a nossa classe TeleopNode, que herda de Node
class MeuTeleopNode(Node):
    def __init__(self):
        # Chamando o construtor da classe pai
        super().__init__('teleop_node')

        # Declarando e inicializando os parâmetros do nó
        self.linear_speed = self.declare_parameter('linear_speed', 0.0).value
        self.angular_speed = self.declare_parameter('angular_speed', 0.0).value
        self.speed_increment = self.declare_parameter('speed_increment', 0.5).value
        self.angular_speed_increment = self.declare_parameter('angular_speed_increment', 0.5).value
        self.velocidades_atuais = [0.0, 0.0, 0.0]  # lin x, lin y, ang z

        # Criando o subscriber para o tópico do teclado
        self.subscription = self.create_subscription(
            String,
            'keyboard_topic',
            self.listener_callback,
            10
        )
        self.subscription

        # Criando o publisher para o tópico de comando de velocidade do robô
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    # Função de callback que será chamada sempre que uma nova mensagem chegar no tópico do teclado
    def listener_callback(self, msg):
        self.get_logger().info(f'Recebido: {msg.data}')

        # Inicializando a mensagem Twist que será enviada ao robô
        twist = Twist()
        twist.linear.x = self.velocidades_atuais[0]
        twist.linear.y = self.velocidades_atuais[1]
        twist.angular.z = self.velocidades_atuais[2]

        # Verificando qual tecla foi pressionada e alterando as velocidades ou publicando a mensagem correspondente
        if msg.data.lower() == 'f':
            self.speed_increment += 0.5
            self.angular_speed_increment += 0.5
            self.get_logger().info(f'Velocidade aumentada. Velocidade linear: {self.linear_speed}, Velocidade Angular: {self.angular_speed}')

        if msg.data.lower() == 'w':
            twist.linear.x = self.velocidades_atuais[0] + self.speed_increment
        elif msg.data.lower() == 's':
            twist.linear.x = self.velocidades_atuais[0] - self.speed_increment
        elif msg.data.lower() == 'a':
            twist.linear.y = self.velocidades_atuais[1] + self.speed_increment
        elif msg.data.lower() == 'd':
            twist.linear.y = self.velocidades_atuais[1] - self.speed_increment
        elif msg.data.lower() == 'q':
            twist.angular.z = self.velocidades_atuais[2] + self.angular_speed_increment
        elif msg.data.lower() == 'e':
            twist.angular.z = self.velocidades_atuais[2] - self.angular_speed_increment
        elif msg.data.lower() == ' ':
            twist = Twist()
            self.get_logger().info('Parada de emergência ativada.')

        self.velocidades_atuais = [twist.linear.x, twist.linear.y, twist.angular.z]
        if msg.data.lower() in ['w', 's', 'a', 'd', 'q', 'e', ' ']:
            self.publisher.publish(twist)


# Função principal que será chamada quando o script for executado
def main(args=None):
    # Inicializando o ROS
    rclpy.init(args=args)

    # Criando a nossa instância do TeleopNode
    meu_teleop_node = MeuTeleopNode()

    try:
        # Entrando no loop de execução do ROS. Isso fará com que as callbacks sejam chamadas até que o nó seja desligado.
        rclpy.spin(meu_teleop_node)
    except KeyboardInterrupt:
        # Se o nó for interrompido por um sinal de interrupção (como CTRL+C), ele sairá do loop de execução
        pass

    # Destruindo o nó e desligando o ROS
    meu_teleop_node.destroy_node()
    rclpy.shutdown()


# Se o script for executado diretamente (em vez de importado), chamamos a função principal
if __name__ == '__main__':
    main()