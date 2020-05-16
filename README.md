# work_test_for_star_staff
1. Downloaad docker, docker-compose
2. Create directory for volume of postgresql
3. Mount your volume to your droplet `ln -s /mnt/<volume_name> ./postgres-data`
4. `docker-compose up -d`
5. Run local script `python3.6 update_data.py --password long_pass_to_db --user cool_user --dumped_logs {logs location for test data}`
6. After run script `python3.6 get_user.py --password long_pass_to_db --user cool_user`for collect record with cashback 
