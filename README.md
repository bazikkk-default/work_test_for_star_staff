# work_test_for_star_staff

1. Install pip requirements.txt
2. Download docker, docker-compose
3. Create directory for volume of postgresql
4. Mount your volume to your droplet `ln -s /mnt/<volume_name> ./postgres-data`
5. `docker-compose up -d`
6. Run local script `python3.6 update_data.py --password long_pass_to_db --user cool_user --dumped_logs {logs location for test data}`
7. After run script `python3.6 get_user.py --password long_pass_to_db --user cool_user`for collect record with cashback 
